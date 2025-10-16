from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.cache import cache
from django.contrib import messages
from django.urls import reverse
from core import DEFAULT_FEATURE_FLAGS
import os
from .models import Thread, ThreadMessage, Block
from moderation.models import Ban, RiskSignal
from listings.models import Listing
from .contact_guard import redact_text


def _ff(name: str) -> bool:
    default = DEFAULT_FEATURE_FLAGS.get(name, False)
    raw = os.environ.get(name)
    return default if raw is None else raw.lower() in ("1", "true", "yes")


def _rate_allow(key: str, limit: int, window_s: int) -> bool:
    now = int(timezone.now().timestamp())
    bucket = now // window_s
    cache_key = f"rl:{key}:{bucket}"
    val = cache.get(cache_key, 0)
    if val >= limit:
        return False
    cache.set(cache_key, val + 1, timeout=window_s)
    return True


@login_required
def start(request, listing_id: int):
    if not _ff('FEATURE_MESSAGING_V1'):
        return HttpResponseForbidden()
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return redirect('marketplace')
    if request.user == listing.store.owner:
        messages.error(request, 'Kendi ilanınıza mesaj gönderemezsiniz.')
        return redirect('listing_detail', listing_id=listing_id)
    # ban guard
    if _ff('FEATURE_BLOCKLIST_P1'):
        active_ban = Ban.objects.filter(user=request.user, active=True, scope__in=['messaging','sitewide']).exclude(expires_at__lt=timezone.now()).exists()
        if active_ban:
            messages.error(request, 'Hesabınız şu anda mesajlaşma için kısıtlı.')
            return redirect('listing_detail', listing_id=listing_id)
    # rate limit: thread_per_h=3
    limits = os.environ.get('MESSAGE_RATE_LIMITS', 'msg_per_5m=10,thread_per_h=3')
    thread_per_h = 3
    for part in limits.split(','):
        if part.startswith('thread_per_h='):
            thread_per_h = int(part.split('=',1)[1])
    if not _rate_allow(f"thread:{request.user.id}", thread_per_h, 3600):
        messages.error(request, 'Çok hızlı! Daha sonra tekrar deneyin.')
        return redirect('listing_detail', listing_id=listing_id)
    # unique open thread or create
    thread, created = Thread.objects.get_or_create(listing=listing, buyer=request.user, seller=listing.store.owner, is_open=True)
    # risk signal: velocity on thread start burst
    if created and _ff('FEATURE_RISK_SIGNALS_P2'):
        # If user already started 3 threads in last hour, emit velocity
        key = f"rl:thread:{request.user.id}:{int(timezone.now().timestamp())//3600}"
        # Using cache value as heuristic (set in _rate_allow)
        # Create signal if many new threads recently
        RiskSignal.objects.create(entity_type='user', entity_id=request.user.id, type='velocity', severity='medium', meta={'context':'thread_start'})
    return redirect('messaging:thread_detail', thread_id=thread.id)


@login_required
def thread_list(request):
    if not _ff('FEATURE_MESSAGING_V1'):
        return HttpResponseForbidden()
    threads = Thread.objects.filter(models.Q(buyer=request.user) | models.Q(seller=request.user)).order_by('-last_message_at','-created_at')
    return render(request, 'messaging/thread_list.html', {'threads': threads})


@login_required
def thread_detail(request, thread_id: int):
    if not _ff('FEATURE_MESSAGING_V1'):
        return HttpResponseForbidden()
    try:
        thread = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        return redirect('messaging:thread_list')
    if request.user not in (thread.buyer, thread.seller):
        return HttpResponseForbidden()
    msgs = thread.messages.all()
    return render(request, 'messaging/thread_detail.html', {'thread': thread, 'messages': msgs})


@login_required
def send_message(request, thread_id: int):
    if not _ff('FEATURE_MESSAGING_V1'):
        return HttpResponseForbidden()
    if request.method != 'POST':
        return redirect('messaging:thread_detail', thread_id=thread_id)
    try:
        thread = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        return redirect('messaging:thread_list')
    if request.user not in (thread.buyer, thread.seller):
        return HttpResponseForbidden()
    # ban/block check
    if _ff('FEATURE_BLOCKLIST_P1'):
        active_ban = Ban.objects.filter(user=request.user, active=True, scope__in=['messaging','sitewide']).exclude(expires_at__lt=timezone.now()).exists()
        if active_ban:
            messages.error(request, 'Hesabınız şu anda mesajlaşma için kısıtlı.')
            return redirect('messaging:thread_detail', thread_id=thread_id)
    # block check
    if Block.objects.filter(blocker=thread.buyer, blocked=thread.seller).exists() or Block.objects.filter(blocker=thread.seller, blocked=thread.buyer).exists():
        messages.error(request, 'Taraflardan biri engellenmiş.')
        return redirect('messaging:thread_detail', thread_id=thread_id)
    text = request.POST.get('message','').strip()
    if not text:
        return redirect('messaging:thread_detail', thread_id=thread_id)
    # rate limit msg_per_5m=10
    limits = os.environ.get('MESSAGE_RATE_LIMITS', 'msg_per_5m=10,thread_per_h=3')
    msg_per_5m = 10
    for part in limits.split(','):
        if part.startswith('msg_per_5m='):
            msg_per_5m = int(part.split('=',1)[1])
    was_rate = not _rate_allow(f"msg:{request.user.id}", msg_per_5m, 300)
    strict = _ff('STRICT_CONTACT_GUARD')
    redacted, has_violation = redact_text(text, strict=strict)
    ThreadMessage.objects.create(thread=thread, sender=request.user, raw_text=text, redacted_text=(redacted if has_violation else None), has_contact_violation=has_violation, was_rate_limited=was_rate)
    thread.last_message_at = timezone.now()
    thread.save(update_fields=['last_message_at'])
    if was_rate:
        messages.error(request, 'Mesaj limitine ulaştınız, lütfen bekleyin.')
        if _ff('FEATURE_RISK_SIGNALS_P2'):
            RiskSignal.objects.create(entity_type='user', entity_id=request.user.id, type='velocity', severity='medium', meta={'context':'message_send'})
    elif has_violation:
        messages.warning(request, 'Kişisel iletişim paylaşımı tespit edildi ve redakte edildi.')
        # Auto-block after 2 violations in 24h
        vkey = f"cg:{request.user.id}:{thread.seller_id if request.user==thread.buyer else thread.buyer_id}"
        vcount = cache.get(vkey, 0) + 1
        cache.set(vkey, vcount, timeout=24*3600)
        if vcount >= 2:
            other_id = thread.seller_id if request.user == thread.buyer else thread.buyer_id
            Block.objects.get_or_create(blocker_id=other_id, blocked_id=request.user.id)
            messages.error(request, 'İletişim paylaşımı ihlali nedeniyle geçici olarak engellendiniz.')
        if _ff('FEATURE_RISK_SIGNALS_P2'):
            RiskSignal.objects.create(entity_type='user', entity_id=request.user.id, type='contact_leak', severity='low', meta={'thread_id': thread.id})
    return redirect('messaging:thread_detail', thread_id=thread_id)


@login_required
def report_message(request, thread_id: int, message_id: int):
    if not _ff('FEATURE_MESSAGING_V1'):
        return HttpResponseForbidden()
    try:
        msg = ThreadMessage.objects.get(id=message_id, thread_id=thread_id)
    except ThreadMessage.DoesNotExist:
        return redirect('messaging:thread_detail', thread_id=thread_id)
    if request.user not in (msg.thread.buyer, msg.thread.seller):
        return HttpResponseForbidden()
    msg.is_reported = True
    msg.save(update_fields=['is_reported'])
    messages.success(request, 'Mesaj raporlandı.')
    return redirect('messaging:thread_detail', thread_id=thread_id)


@login_required
def block_user(request, user_id: int):
    if not _ff('FEATURE_MESSAGING_V1'):
        return HttpResponseForbidden()
    Block.objects.get_or_create(blocker=request.user, blocked_id=user_id)
    messages.success(request, 'Kullanıcı engellendi.')
    return redirect('messaging:thread_list')


@login_required
def mark_read(request, thread_id: int):
    if not _ff('FEATURE_MESSAGING_V1'):
        return HttpResponseForbidden()
    try:
        thread = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        return redirect('messaging:thread_list')
    if request.user not in (thread.buyer, thread.seller):
        return HttpResponseForbidden()
    is_buyer = request.user == thread.buyer
    qs = ThreadMessage.objects.filter(thread=thread).exclude(sender=request.user)
    if is_buyer:
        qs.update(read_by_buyer=True)
    else:
        qs.update(read_by_seller=True)
    return redirect('messaging:thread_detail', thread_id=thread_id)

# Create your views here.

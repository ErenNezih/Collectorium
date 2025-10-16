from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.cache import cache
from django.contrib import messages
from core import DEFAULT_FEATURE_FLAGS
import os
from .forms import ReportForm
from .models import Report, ModerationAction


def _ff(name: str) -> bool:
    default = DEFAULT_FEATURE_FLAGS.get(name, False)
    raw = os.environ.get(name)
    return default if raw is None else raw.lower() in ("1", "true", "yes")


def _rate_allow(key: str, limit: int, window_s: int) -> bool:
    from django.utils import timezone
    now = int(timezone.now().timestamp())
    bucket = now // window_s
    ck = f"rl:{key}:{bucket}"
    val = cache.get(ck, 0)
    if val >= limit:
        return False
    cache.set(ck, val + 1, timeout=window_s)
    return True


@login_required
def report(request, target_type: str, target_id: int):
    if not _ff('FEATURE_REPORTING_P0'):
        return HttpResponseForbidden()
    if request.method == 'POST':
        # rate limit: 5 per hour
        if not _rate_allow(f"report:{request.user.id}", 5, 3600):
            messages.error(request, 'Çok sık şikayet gönderildi. Lütfen sonra tekrar deneyin.')
            return redirect('home')
        form = ReportForm(request.POST)
        if form.is_valid():
            # dedupe per day
            from datetime import date
            today = date.today()
            exists = Report.objects.filter(reporter=request.user, target_type=target_type, target_id=target_id, created_at__date=today).exists()
            if exists:
                messages.error(request, 'Bu hedef için bugün zaten şikayet oluşturdunuz.')
                return redirect('home')
            rep = form.save(commit=False)
            rep.reporter = request.user
            rep.target_type = target_type
            rep.target_id = target_id
            rep.save()
            messages.success(request, 'Şikayetiniz alınmıştır.')
            return redirect('home')
    else:
        form = ReportForm()
    return render(request, 'moderation/report_form.html', {'form': form, 'target_type': target_type, 'target_id': target_id})


# Create your views here.

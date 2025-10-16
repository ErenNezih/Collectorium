from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import os
from core import DEFAULT_FEATURE_FLAGS
from .models import Payment, PaymentTransaction, WebhookEvent
from orders.models import Order
from decimal import Decimal
import hashlib
import hmac
import json


def _ff(name: str) -> bool:
    default = DEFAULT_FEATURE_FLAGS.get(name, False)
    raw = os.environ.get(name)
    return default if raw is None else raw.lower() in ("1", "true", "yes")


def start(request, order_id: int):
    if not _ff("P0_FEATURES_ENABLED") or not _ff("FEATURE_PAYMENTS_SANDBOX"):
        return redirect("orders:order_create")
    # Create Payment intent (sandbox placeholder)
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect("cart:cart_detail")
    # idempotent get-or-create by order
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            'provider': 'iyzico',
            'payment_id': f'sandbox-{order.id}',
            'status': 'initiated',
            'amount': Decimal(order.total),
            'currency': order.currency,
            'three_ds_required': True,
        }
    )
    request.session['payment_id'] = payment.payment_id
    return render(request, "payments/start.html", {"order_id": order_id, "payment": payment})


def return_view(request):
    # Handle provider return (3DS success/failed)
    success = request.GET.get("success") == "1"
    order_id = request.session.get('order_id')
    if success and order_id:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            messages.error(request, "Sipariş bulunamadı.")
            return redirect('cart:cart_detail')
        # Update payment to captured (sandbox immediate capture)
        try:
            payment = Payment.objects.get(order=order)
        except Payment.DoesNotExist:
            payment = None
        if payment:
            payment.status = 'captured'
            payment.captured_at = timezone.now()
            payment.save(update_fields=['status', 'captured_at', 'updated_at'])
            # record tx idempotently
            idem = hashlib.md5(f"capture-{payment.payment_id}".encode()).hexdigest()
            PaymentTransaction.objects.get_or_create(
                payment=payment,
                idempotency_key=idem,
                defaults={'type': 'capture', 'amount': payment.amount, 'status': 'succeeded'}
            )
        # Mark order paid (triggers sale price point via signal)
        order.status = 'paid'
        order.save(update_fields=['status'])
        messages.success(request, "Ödeme başarıyla doğrulandı (sandbox).")
        return redirect("orders:order_created")
    messages.error(request, "Ödeme başarısız veya iptal edildi.")
    return redirect("cart:cart_detail")


@csrf_exempt
@require_POST
def webhook(request):
    # Minimal idempotent webhook receiver with HMAC validation (sandbox style)
    dedupe_key = request.headers.get("X-Event-Id") or request.META.get("HTTP_X_EVENT_ID")
    provider = "iyzico"
    event_type = request.headers.get("X-Event-Type", "unknown")
    signature = request.headers.get("X-Signature", "")
    try:
        body = request.body.decode("utf-8")
        payload = json.loads(body) if body else {}
    except Exception:
        payload = request.POST.dict() if request.POST else {}

    if not dedupe_key:
        return HttpResponseBadRequest("missing dedupe key")

    obj, created = WebhookEvent.objects.get_or_create(
        dedupe_key=dedupe_key,
        defaults={
            "provider": provider,
            "event_type": event_type,
            "signature": signature,
            "payload": payload,
            "result": "skipped",
        },
    )
    if not created:
        return JsonResponse({"status": "duplicate"})

    # HMAC signature check (if provided)
    secret = os.environ.get('IYZICO_SECRET', '')
    if secret and signature:
        calc = hmac.new(secret.encode(), msg=(body if body else json.dumps(payload)).encode(), digestmod='sha256').hexdigest()
        if not hmac.compare_digest(calc, signature):
            obj.result = "err"
            obj.save(update_fields=["result"])
            return HttpResponseBadRequest("invalid signature")

    # Route to handler (simple sandbox types)
    try:
        if event_type == 'payment.captured' and payload.get('order_id'):
            order_id = int(payload['order_id'])
            order = Order.objects.get(id=order_id)
            payment = Payment.objects.filter(order=order).first()
            if payment and payment.status != 'captured':
                payment.status = 'captured'
                payment.captured_at = timezone.now()
                payment.save(update_fields=['status', 'captured_at', 'updated_at'])
                idem = hashlib.md5(f"capture-{payment.payment_id}".encode()).hexdigest()
                PaymentTransaction.objects.get_or_create(
                    payment=payment,
                    idempotency_key=idem,
                    defaults={'type': 'capture', 'amount': payment.amount, 'status': 'succeeded'}
                )
            if order.status != 'paid':
                order.status = 'paid'
                order.save(update_fields=['status'])
    except Exception:
        obj.result = "err"
        obj.save(update_fields=["result"])
        return JsonResponse({"status": "error"}, status=500)

    obj.result = "ok"
    obj.save(update_fields=["result"])
    return JsonResponse({"status": "ok"})

# Create your views here.

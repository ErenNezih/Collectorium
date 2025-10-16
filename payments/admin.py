from django.contrib import admin
from .models import Payment, PaymentTransaction, WebhookEvent, LedgerEntry, RefundRequest


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "provider", "payment_id", "status", "amount", "currency", "created_at")
    search_fields = ("payment_id", "order__id", "provider")
    list_filter = ("provider", "status", "currency", "created_at")
    readonly_fields = ("created_at", "updated_at", "authorized_at", "captured_at", "refunded_at")


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("payment", "type", "amount", "status", "idempotency_key", "created_at")
    search_fields = ("payment__payment_id", "idempotency_key", "ext_ref")
    list_filter = ("type", "status", "created_at")
    readonly_fields = ("created_at",)


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ("provider", "event_type", "dedupe_key", "result", "created_at")
    search_fields = ("event_type", "dedupe_key", "provider")
    list_filter = ("provider", "result", "created_at")
    readonly_fields = ("created_at", "processed_at")


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("entity", "seller", "order", "direction", "amount", "currency", "created_at")
    search_fields = ("order__id", "seller__name")
    list_filter = ("entity", "direction", "currency", "created_at")
    readonly_fields = ("created_at",)


@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ("order", "type", "status", "decided_by", "decided_at", "created_at")
    search_fields = ("order__id",)
    list_filter = ("type", "status", "created_at")
    readonly_fields = ("created_at", "decided_at")

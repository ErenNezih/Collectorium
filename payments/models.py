from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Payment(models.Model):
    """Payment lifecycle for an Order (provider-agnostic).

    Order 1–1 Payment in P0 (single payment per order).
    """

    STATUS_CHOICES = (
        ("initiated", "Initiated"),
        ("authorized", "Authorized"),
        ("captured", "Captured"),
        ("refunded", "Refunded"),
        ("failed", "Failed"),
    )

    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, related_name="payment")
    provider = models.CharField(max_length=50, db_index=True)
    payment_id = models.CharField(max_length=100, unique=True, help_text="External provider payment reference")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="initiated", db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="TRY")

    three_ds_required = models.BooleanField(default=False)
    three_ds_status = models.CharField(max_length=50, blank=True, default="")

    authorized_at = models.DateTimeField(null=True, blank=True)
    captured_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    raw_payload = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["provider", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def mark_authorized(self):
        self.status = "authorized"
        self.authorized_at = timezone.now()
        self.save(update_fields=["status", "authorized_at", "updated_at"])

    def mark_captured(self):
        self.status = "captured"
        self.captured_at = timezone.now()
        self.save(update_fields=["status", "captured_at", "updated_at"])

    def mark_refunded(self):
        self.status = "refunded"
        self.refunded_at = timezone.now()
        self.save(update_fields=["status", "refunded_at", "updated_at"])

    def __str__(self) -> str:
        return f"Payment<{self.provider}:{self.payment_id}:{self.status}>"


class PaymentTransaction(models.Model):
    """Atomic transaction event for a Payment (auth/capture/refund/void/fail)."""

    TYPE_CHOICES = (
        ("auth", "Authorize"),
        ("capture", "Capture"),
        ("refund", "Refund"),
        ("void", "Void"),
        ("fail", "Fail"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed"),
    )

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    idempotency_key = models.CharField(max_length=120, unique=True)
    ext_ref = models.CharField(max_length=120, blank=True, default="", help_text="External reference id")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    raw = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["payment", "type"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        return f"PaymentTx<{self.payment_id}:{self.type}:{self.status}>"


class WebhookEvent(models.Model):
    """Raw webhook events with deduplication and processing result."""

    RESULT_CHOICES = (
        ("ok", "Processed OK"),
        ("err", "Processed with Error"),
        ("skipped", "Skipped"),
    )

    provider = models.CharField(max_length=50, db_index=True)
    event_type = models.CharField(max_length=100)
    signature = models.CharField(max_length=200, blank=True, default="")
    payload = models.JSONField()
    dedupe_key = models.CharField(max_length=180, unique=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["provider", "event_type"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f"Webhook<{self.provider}:{self.event_type}:{self.dedupe_key}>"


class LedgerEntry(models.Model):
    """Double-entry style ledger entries for platform and sellers."""

    ENTITY_CHOICES = (("platform", "Platform"), ("seller", "Seller"))
    DIRECTION_CHOICES = (("dr", "Debit"), ("cr", "Credit"))

    entity = models.CharField(max_length=20, choices=ENTITY_CHOICES)
    seller = models.ForeignKey("stores.Store", on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="ledger_entries")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES)
    currency = models.CharField(max_length=3, default="TRY")
    memo = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["order", "entity"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f"Ledger<{self.entity}:{self.direction}:{self.amount} {self.currency}>"


class RefundRequest(models.Model):
    """Minimal refund/dispute request tracking (P0 scope)."""

    TYPE_CHOICES = (("full", "Full"), ("partial", "Partial"))
    STATUS_CHOICES = (("open", "Open"), ("approved", "Approved"), ("denied", "Denied"))

    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="refund_requests")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    reason = models.TextField(blank=True, default="")
    evidence_urls = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    decided_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def approve(self, user: User | None = None):
        self.status = "approved"
        self.decided_by = user
        self.decided_at = timezone.now()
        self.save(update_fields=["status", "decided_by", "decided_at"])

    def deny(self, user: User | None = None):
        self.status = "denied"
        self.decided_by = user
        self.decided_at = timezone.now()
        self.save(update_fields=["status", "decided_by", "decided_at"])

    def __str__(self) -> str:
        return f"RefundRequest<{self.order_id}:{self.type}:{self.status}>"

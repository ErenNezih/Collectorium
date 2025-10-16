from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Report(models.Model):
    TARGET_CHOICES = (("listing","Listing"),("message","Message"),("user","User"))
    STATUS_CHOICES = (("open","Open"),("actioned","Actioned"),("closed","Closed"))

    reporter = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reports')
    target_type = models.CharField(max_length=20, choices=TARGET_CHOICES, db_index=True)
    target_id = models.PositiveIntegerField(db_index=True)
    reason = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['target_type','target_id','status']),
        ]

    def __str__(self):
        return f"Report<{self.target_type}:{self.target_id}:{self.status}>"


class ModerationAction(models.Model):
    ACTION_CHOICES = (("hide_listing","Hide Listing"),("delete_message","Delete Message"),("warn_user","Warn User"),("ban_user","Ban User"),("no_action","No Action"))
    SEVERITY_CHOICES = (("low","Low"),("medium","Medium"),("high","High"))

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='actions')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='low')
    notes = models.TextField(blank=True, null=True)
    actor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='moderation_actions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Action<{self.action}:{self.severity}>"


class RiskSignal(models.Model):
    TYPE_CHOICES = (("velocity","Velocity"),("high_amount","High Amount"),("first_order","First Order"),("contact_leak","Contact Leak"))
    SEVERITY_CHOICES = (("low","Low"),("medium","Medium"),("high","High"))

    entity_type = models.CharField(max_length=20, db_index=True)  # order|user|listing
    entity_id = models.PositiveIntegerField(db_index=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='low', db_index=True)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entity_type','entity_id','type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Risk<{self.type}:{self.severity}>"


class Ban(models.Model):
    SCOPE_CHOICES = (("messaging","Messaging"),("purchase","Purchase"),("sitewide","Sitewide"))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bans')
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, db_index=True)
    reason = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='bans_created', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user','scope','active']),
        ]

    def __str__(self):
        return f"Ban<{self.user_id}:{self.scope}:{'active' if self.active else 'inactive'}>"

# Create your models here.

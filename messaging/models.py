from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class Thread(models.Model):
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='threads', db_index=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads_as_seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads_as_buyer')
    is_open = models.BooleanField(default=True)
    last_message_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_message_at', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['listing', 'buyer', 'seller'],
                condition=Q(is_open=True),
                name='uniq_open_thread_per_listing_buyer_seller',
            )
        ]

    def __str__(self):
        return f"Thread<{self.listing_id}:{self.buyer_id}->{self.seller_id}>"


class ThreadMessage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages', db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_messages', db_index=True)
    raw_text = models.TextField()
    redacted_text = models.TextField(null=True, blank=True)
    has_contact_violation = models.BooleanField(default=False)
    was_rate_limited = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    read_by_buyer = models.BooleanField(default=False)
    read_by_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"TM<{self.thread_id}:{self.sender_id}>"


class Block(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocks_initiated')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocks_received')
    reason = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['blocker', 'blocked']),
        ]

    def __str__(self):
        return f"Block<{self.blocker_id}->{self.blocked_id}>"

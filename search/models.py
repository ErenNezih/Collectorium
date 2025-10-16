from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SavedSearch(models.Model):
    FREQ_CHOICES = (("daily", "Daily"), ("weekly", "Weekly"))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_searches", db_index=True)
    name = models.CharField(max_length=80)
    querystring = models.TextField()
    frequency = models.CharField(max_length=10, choices=FREQ_CHOICES, default="daily", db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    qhash = models.CharField(max_length=32, blank=True, default="", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [("user", "name")]
        indexes = [
            models.Index(fields=["user", "active", "frequency"], name="saved_user_active_freq_idx"),
        ]

    def __str__(self):
        return f"SavedSearch<{self.user_id}:{self.name}>"


class PricePoint(models.Model):
    KIND_CHOICES = (("list", "List"), ("sale", "Sale"))

    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='price_points', db_index=True)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, db_index=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='TRY')
    at = models.DateTimeField(db_index=True)
    source = models.CharField(max_length=20, default='created')

    class Meta:
        ordering = ['-at']
        indexes = [
            models.Index(fields=['listing', 'at'], name='pp_listing_at_idx'),
            models.Index(fields=['listing', 'kind', 'at'], name='pp_listing_kind_at_idx'),
        ]

    def __str__(self):
        return f"PricePoint<{self.listing_id}:{self.kind}:{self.price}>"

# Create your models here.

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stores')
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    bio = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Aggregated rating (flag: FEATURE_STORE_REVIEWS)
    rating_avg = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    rating_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class StorePolicy(models.Model):
    store = models.OneToOneField('stores.Store', on_delete=models.CASCADE, related_name='policy')
    return_policy_text = models.TextField(blank=True, null=True)
    shipping_policy_text = models.TextField(blank=True, null=True)
    contact_hours = models.CharField(max_length=120, blank=True, null=True)
    handling_time_days = models.PositiveIntegerField(blank=True, null=True)
    extra_notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Policy<{self.store.name}>"
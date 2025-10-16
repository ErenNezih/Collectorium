from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Yeni'),
        ('like_new', 'Sıfıra Yakın'),
        ('good', 'İyi'),
        ('fair', 'Orta'),
        ('poor', 'Kötü'),
    ]

    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name='listings')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    currency = models.CharField(max_length=3, default='TRY')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    stock = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Esnek kategori alanları için (Search V1/P1): JSONB
    attributes = models.JSONField(default=dict, blank=True)
    # Lokasyon alanları (P2 Map Search)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"{self.listing.title} - Image {self.id}"


class Favorite(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'listing']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"
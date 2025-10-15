from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'listing']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.listing.title} x{self.quantity}"

    @property
    def total_price(self):
        return self.listing.price * self.quantity

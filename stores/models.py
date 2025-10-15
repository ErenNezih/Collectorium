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

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
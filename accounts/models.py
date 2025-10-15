from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (("buyer","Buyer"),("seller","Seller"),("admin","Admin"))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="buyer")
    store_name = models.CharField(max_length=120, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self): 
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_title = models.CharField(max_length=100, help_text="Örn: Ev, İş")
    country = models.CharField(max_length=100, default="Türkiye")
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    full_address = models.TextField()
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', '-created_at']
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.user.username} - {self.address_title}"

    def save(self, *args, **kwargs):
        # Eğer bu adres default olarak işaretleniyorsa, diğer adreslerin default'unu kaldır
        if self.is_default:
            # Mevcut adres dışındaki diğer tüm adreslerin 'is_default' bayrağını kaldır.
            # Bu, gereksiz veritabanı güncellemelerini önler.
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from stores.models import Store

User = get_user_model()


@receiver(post_save, sender=User)
def create_store_for_seller(sender, instance, created, **kwargs):
    """
    Seller rolünde kayıt olan kullanıcılar için otomatik mağaza oluşturur.
    """
    if created and instance.role == 'seller':
        # Kullanıcıya ait bir mağaza yoksa oluştur
        if not Store.objects.filter(owner=instance).exists():
            store_name = instance.store_name or f"{instance.username}'s Store"
            slug_base = slugify(store_name)
            slug = slug_base
            
            # Benzersiz slug oluştur
            counter = 1
            while Store.objects.filter(slug=slug).exists():
                slug = f"{slug_base}-{counter}"
                counter += 1
            
            Store.objects.create(
                owner=instance,
                name=store_name,
                slug=slug
            )


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Listing
from search.models import PricePoint


@receiver(post_save, sender=Listing)
def create_initial_list_pricepoint(sender, instance: Listing, created: bool, **kwargs):
    from core import DEFAULT_FEATURE_FLAGS
    import os
    def _ff(name: str) -> bool:
        default = DEFAULT_FEATURE_FLAGS.get(name, False)
        raw = os.environ.get(name)
        return default if raw is None else raw.lower() in ("1", "true", "yes")
    if not _ff('FEATURE_PRICE_HISTORY'):
        return
    if created:
        # idempotent: avoid duplicate by checking earliest point
        exists = PricePoint.objects.filter(listing=instance, kind='list').exists()
        if not exists:
            PricePoint.objects.create(
                listing=instance,
                kind='list',
                price=instance.price,
                currency=instance.currency,
                at=timezone.now(),
                source='created',
            )




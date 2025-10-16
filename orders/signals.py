from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Order, OrderItem
from search.models import PricePoint
from core import DEFAULT_FEATURE_FLAGS
import os


def _ff(name: str) -> bool:
    default = DEFAULT_FEATURE_FLAGS.get(name, False)
    raw = os.environ.get(name)
    return default if raw is None else raw.lower() in ("1", "true", "yes")


@receiver(post_save, sender=Order)
def create_sale_pricepoints_on_paid(sender, instance: Order, created: bool, **kwargs):
    if not _ff('FEATURE_PRICE_HISTORY'):
        return
    if created:
        return
    if instance.status not in ('paid', 'refunded'):
        return
    items = OrderItem.objects.filter(order=instance)
    for oi in items:
        exists = PricePoint.objects.filter(listing=oi.listing, kind='sale', at__date=instance.created_at.date()).exists()
        if not exists:
            PricePoint.objects.create(
                listing=oi.listing,
                kind='sale',
                price=oi.price_snapshot,
                currency=instance.currency,
                at=instance.created_at or timezone.now(),
                source='order_capture',
            )



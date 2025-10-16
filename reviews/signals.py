from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import Review
from stores.models import Store
from core import DEFAULT_FEATURE_FLAGS
import os


def _ff(name: str) -> bool:
    default = DEFAULT_FEATURE_FLAGS.get(name, False)
    raw = os.environ.get(name)
    return default if raw is None else raw.lower() in ("1", "true", "yes")


def _recompute_store_rating(store: Store):
    agg = store.listings.aggregate(avg=Avg('reviews__rating'), cnt=Count('reviews'))
    store.rating_avg = agg['avg'] or 0
    store.rating_count = agg['cnt'] or 0
    store.save(update_fields=['rating_avg', 'rating_count'])


@receiver(post_save, sender=Review)
def on_review_save(sender, instance: Review, created: bool, **kwargs):
    if not _ff('FEATURE_STORE_REVIEWS'):
        return
    _recompute_store_rating(instance.listing.store)


@receiver(post_delete, sender=Review)
def on_review_delete(sender, instance: Review, **kwargs):
    if not _ff('FEATURE_STORE_REVIEWS'):
        return
    _recompute_store_rating(instance.listing.store)



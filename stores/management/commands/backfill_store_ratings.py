from django.core.management.base import BaseCommand
from django.db.models import Avg, Count
from stores.models import Store


class Command(BaseCommand):
    help = "Backfill store rating aggregates from reviews"

    def handle(self, *args, **options):
        updated = 0
        for store in Store.objects.all():
            agg = store.listings.aggregate(avg=Avg('reviews__rating'), cnt=Count('reviews'))
            store.rating_avg = agg['avg'] or 0
            store.rating_count = agg['cnt'] or 0
            store.save(update_fields=['rating_avg', 'rating_count'])
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} stores"))



from django.core.management.base import BaseCommand
from listings.models import Listing
import random

CITIES = [
    ("İstanbul", ["Kadıköy", "Beşiktaş", "Üsküdar", "Şişli"]),
    ("Ankara", ["Çankaya", "Keçiören", "Yenimahalle"]),
    ("İzmir", ["Konak", "Karşıyaka", "Bornova"]),
]


class Command(BaseCommand):
    help = "Seed city/district fields for existing listings (randomized)"

    def handle(self, *args, **options):
        updated = 0
        for li in Listing.objects.all():
            if not li.city or not li.district:
                city, dists = random.choice(CITIES)
                li.city = city
                li.district = random.choice(dists)
                li.save(update_fields=["city", "district"])
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Location seeded for {updated} listings"))



from django.core.management.base import BaseCommand
from django.utils import timezone
from listings.models import Listing
from orders.models import Order, OrderItem
from search.models import PricePoint


class Command(BaseCommand):
    help = "Backfill price points from existing listings and orders"

    def handle(self, *args, **options):
        created_list = 0
        for li in Listing.objects.all():
            if not PricePoint.objects.filter(listing=li, kind='list').exists():
                PricePoint.objects.create(listing=li, kind='list', price=li.price, currency=li.currency, at=li.created_at or timezone.now(), source='backfill')
                created_list += 1
        self.stdout.write(self.style.SUCCESS(f"List points created: {created_list}"))

        created_sale = 0
        paid_orders = Order.objects.filter(status__in=['paid', 'refunded'])
        for oi in OrderItem.objects.filter(order__in=paid_orders):
            if not PricePoint.objects.filter(listing=oi.listing, kind='sale', at__date=oi.order.created_at.date()).exists():
                PricePoint.objects.create(listing=oi.listing, kind='sale', price=oi.price_snapshot, currency=oi.order.currency, at=oi.order.created_at, source='backfill')
                created_sale += 1
        self.stdout.write(self.style.SUCCESS(f"Sale points created: {created_sale}"))




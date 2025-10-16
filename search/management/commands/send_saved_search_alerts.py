from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from urllib.parse import urlencode
from datetime import timedelta
from search.models import SavedSearch
from listings.models import Listing
from django.db.models import Q


class Command(BaseCommand):
    help = "Send saved search alerts (console backend acceptable)"

    def handle(self, *args, **options):
        now = timezone.now()
        sent_for_user = set()
        qs = SavedSearch.objects.filter(active=True)
        for item in qs:
            window = timedelta(days=1) if item.frequency == 'daily' else timedelta(days=7)
            since = item.last_run_at or (now - window)
            # parse querystring minimally
            params = {}
            for kv in item.querystring.split('&'):
                if not kv:
                    continue
                parts = kv.split('=', 1)
                if len(parts) == 2:
                    k, v = parts
                    params[k] = v
            listings = Listing.objects.filter(is_active=True)
            if 'q' in params:
                q = params['q']
                listings = listings.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(product__name__icontains=q) | Q(product__brand__icontains=q))
            if 'category' in params:
                listings = listings.filter(product__category__slug=params['category'])
            if 'brand' in params:
                listings = listings.filter(product__brand__icontains=params['brand'])
            if 'condition' in params:
                listings = listings.filter(condition=params['condition'])
            if 'price_min' in params:
                listings = listings.filter(price__gte=params['price_min'])
            if 'price_max' in params:
                listings = listings.filter(price__lte=params['price_max'])
            listings = listings.filter(created_at__gt=since).order_by('-created_at')[:10]

            if not listings.exists():
                item.last_run_at = now
                item.save(update_fields=['last_run_at'])
                continue

            # per-user quota: 1 email per run
            if item.user_id in sent_for_user:
                item.last_run_at = now
                item.save(update_fields=['last_run_at'])
                continue

            subject = "Yeni ilanlar hazır"
            lines = ["Son 24s/7g içinde yeni ilanlar:"]
            base_url = "/search/?" + item.querystring
            for li in listings:
                lines.append(f"- {li.title} (/listing/{li.id}/)")
            body = "\n".join(lines)
            # console backend acceptable
            send_mail(subject, body, None, [item.user.email or "noreply@example.com"], fail_silently=True)
            sent_for_user.add(item.user_id)
            item.last_run_at = now
            item.save(update_fields=['last_run_at'])
        self.stdout.write(self.style.SUCCESS("Saved search alerts processed."))




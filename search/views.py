from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.db.models import Q, Count, Avg
from listings.models import Listing
from catalog.models import Category, Product
from core import DEFAULT_FEATURE_FLAGS
import os
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from .models import SavedSearch
try:
    from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
    from django.contrib.postgres.search import TrigramSimilarity
except Exception:  # SQLite/dev fallback
    SearchVector = SearchQuery = SearchRank = TrigramSimilarity = None


def _ff(name: str) -> bool:
    default = DEFAULT_FEATURE_FLAGS.get(name, False)
    raw = os.environ.get(name)
    return default if raw is None else raw.lower() in ("1", "true", "yes")

def results(request):
    if not _ff('FEATURE_SEARCH_V1'):
        return render(request, 'search/results.html', {"disabled": True})

    q = request.GET.get('q', '')
    category_slug = request.GET.get('category')
    brand = request.GET.get('brand')
    series = request.GET.get('series')
    set_name = request.GET.get('set')
    rarity = request.GET.get('rarity')
    grade = request.GET.get('grade')
    scale = request.GET.get('scale')
    condition = request.GET.get('condition')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    seller_rating_min = request.GET.get('seller_rating_min')
    sort = request.GET.get('sort', 'relevance')

    listings = Listing.objects.filter(is_active=True).select_related('store', 'product', 'product__category').prefetch_related('images')

    if category_slug:
        listings = listings.filter(product__category__slug=category_slug)
    if q:
        # Postgres FTS / Trigram if available; otherwise icontains fallback
        if connection.vendor == 'postgresql' and SearchVector and SearchQuery and SearchRank:
            vector = (
                SearchVector('title', weight='A') +
                SearchVector('description', weight='B') +
                SearchVector('product__name', weight='A') +
                SearchVector('product__brand', weight='B')
            )
            query = SearchQuery(q)
            listings = listings.annotate(rank=SearchRank(vector, query))
            listings = listings.filter(rank__gte=0.1).order_by('-rank', '-created_at')
        else:
            listings = listings.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(product__name__icontains=q) |
                Q(product__brand__icontains=q)
            )
    if brand:
        listings = listings.filter(product__brand__icontains=brand)
    # Kategoriye özel facetler (attributes JSONB)
    if series:
        listings = listings.filter(attributes__series__iexact=series)
    if set_name:
        listings = listings.filter(attributes__set__iexact=set_name)
    if rarity:
        listings = listings.filter(attributes__rarity__iexact=rarity)
    if grade:
        listings = listings.filter(attributes__grade__iexact=grade)
    if scale:
        listings = listings.filter(attributes__scale__iexact=scale)
    if condition:
        listings = listings.filter(condition=condition)
    if price_min:
        listings = listings.filter(price__gte=price_min)
    if price_max:
        listings = listings.filter(price__lte=price_max)
    if seller_rating_min:
        try:
            thr = float(seller_rating_min)
            listings = listings.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=thr)
        except ValueError:
            pass

    if sort == 'newest':
        listings = listings.order_by('-created_at')
    elif sort == 'price_asc':
        listings = listings.order_by('price')
    elif sort == 'price_desc':
        listings = listings.order_by('-price')
    elif sort == 'rating':
        listings = listings.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating', '-created_at')
    elif sort == 'popular':
        listings = listings.annotate(review_count=Count('reviews')).order_by('-review_count', '-created_at')
    else:  # relevance (basit/FTS)
        if q and connection.vendor == 'postgresql' and TrigramSimilarity:
            listings = listings.annotate(
                similarity=TrigramSimilarity('title', q) + TrigramSimilarity('description', q)
            ).order_by('-similarity', '-created_at')
        else:
            listings = listings.order_by('-created_at')

    # Facet seçenekleri (örnek: brand)
    brand_options = []
    try:
        if category_slug:
            cat = Category.objects.get(slug=category_slug)
            brand_options = list(Product.objects.filter(category=cat).exclude(brand__isnull=True).exclude(brand__exact='').values_list('brand', flat=True).distinct()[:50])
        else:
            brand_options = list(Product.objects.exclude(brand__isnull=True).exclude(brand__exact='').values_list('brand', flat=True).distinct()[:50])
    except Category.DoesNotExist:
        pass

    # Kategori listesi (form için)
    categories = Category.objects.order_by('name')

    # Sayfalama
    from django.core.paginator import Paginator
    paginator = Paginator(listings, 24)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'search/results.html', {
        'q': q,
        'category_slug': category_slug,
        'brand': brand,
        'series': series,
        'set_name': set_name,
        'rarity': rarity,
        'grade': grade,
        'scale': scale,
        'condition': condition,
        'price_min': price_min,
        'price_max': price_max,
        'seller_rating_min': seller_rating_min,
        'sort': sort,
        'brand_options': brand_options,
        'categories': categories,
        'page_obj': page_obj,
        'listings': page_obj,
    })


def _require_flag_or_403(flag_name: str):
    if not _ff(flag_name):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
    return None


@login_required
def saved_search_create(request):
    guard = _require_flag_or_403('FEATURE_SAVED_SEARCHES')
    if guard:
        return guard
    if request.method == 'POST':
        name = request.POST.get('name') or 'Kaydedilmiş Arama'
        # querystring: existing GET params of /search/
        qs = request.POST.get('querystring') or request.META.get('HTTP_REFERER', '')
        if '?' in qs:
            qs = qs.split('?', 1)[1]
        ss, _ = SavedSearch.objects.get_or_create(user=request.user, name=name, defaults={
            'querystring': qs,
        })
        ss.querystring = qs
        ss.save(update_fields=['querystring', 'updated_at'])
        return HttpResponseRedirect(reverse('search:saved_list'))
    # fallback redirect
    return HttpResponseRedirect(reverse('search:saved_list'))


@login_required
def saved_search_list(request):
    guard = _require_flag_or_403('FEATURE_SAVED_SEARCHES')
    if guard:
        return guard
    items = SavedSearch.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'search/saved_list.html', {'items': items})


@login_required
def saved_search_update(request, pk: int):
    guard = _require_flag_or_403('FEATURE_SAVED_SEARCHES')
    if guard:
        return guard
    try:
        ss = SavedSearch.objects.get(pk=pk, user=request.user)
    except SavedSearch.DoesNotExist:
        from django.http import Http404
        raise Http404
    if request.method == 'POST':
        ss.name = request.POST.get('name', ss.name)[:80]
        ss.frequency = request.POST.get('frequency', ss.frequency)
        ss.active = request.POST.get('active') == 'on'
        ss.save()
        return HttpResponseRedirect(reverse('search:saved_list'))
    return render(request, 'search/saved_form.html', {'item': ss})


@login_required
def saved_search_delete(request, pk: int):
    guard = _require_flag_or_403('FEATURE_SAVED_SEARCHES')
    if guard:
        return guard
    try:
        ss = SavedSearch.objects.get(pk=pk, user=request.user)
    except SavedSearch.DoesNotExist:
        from django.http import Http404
        raise Http404
    if request.method == 'POST':
        ss.delete()
        return HttpResponseRedirect(reverse('search:saved_list'))
    return render(request, 'search/saved_form.html', {'item': ss, 'delete_confirm': True})


def compare(request):
    if not _ff('FEATURE_COMPARE'):
        return HttpResponseForbidden()
    ids = request.GET.get('ids', '')
    try:
        id_list = [int(x) for x in ids.split(',') if x][:4]
    except ValueError:
        id_list = []
    listings = list(Listing.objects.filter(id__in=id_list).select_related('product__category', 'store').prefetch_related('images'))
    error = None
    if listings:
        cat_ids = {li.product.category_id for li in listings}
        if len(cat_ids) > 1:
            error = 'Yalnızca aynı kategorideki ilanlar karşılaştırılabilir.'
    return render(request, 'search/compare.html', {'listings': listings, 'error': error})


@cache_page(60 * 5)
def price_trends(request, category_slug: str):
    if not _ff('FEATURE_PRICE_HISTORY'):
        return HttpResponseForbidden()
    try:
        cat = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        from django.http import Http404
        raise Http404
    from django.utils import timezone
    from datetime import timedelta
    window = request.GET.get('w', '90d')
    days = 365 if window == '1y' else (90 if window == '90d' else 30)
    since = timezone.now() - timedelta(days=days)
    # Gather sale first, fallback to list
    from search.models import PricePoint
    qs = PricePoint.objects.filter(listing__product__category=cat, at__gte=since)
    sale_qs = qs.filter(kind='sale')
    pp = sale_qs if sale_qs.exists() else qs
    vals = list(pp.values_list('price', flat=True))
    stats = {}
    if vals:
        # Keep Decimal precision
        sv = sorted(vals)
        n = len(sv)
        mid = n // 2
        median = (sv[mid] if n % 2 else (sv[mid - 1] + sv[mid]) / 2)
        p90_idx = max(0, int(n * 0.9) - 1)
        stats = {
            'median': median,
            'min': sv[0],
            'max': sv[-1],
            'p90': sv[p90_idx],
        }
    return render(request, 'search/price_trends.html', {'category': cat, 'stats': stats, 'window': window})


def map_search(request):
    if not _ff('FEATURE_MAP_SEARCH'):
        return HttpResponseForbidden()
    city = request.GET.get('city')
    district = request.GET.get('district')
    qs = Listing.objects.filter(is_active=True)
    if city:
        qs = qs.filter(city__iexact=city)
    if district:
        qs = qs.filter(district__iexact=district)
    from django.core.paginator import Paginator
    paginator = Paginator(qs.select_related('store', 'product').prefetch_related('images'), 24)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'search/map_search.html', {'page_obj': page_obj, 'city': city, 'district': district})

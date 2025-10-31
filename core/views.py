from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
import os
from . import DEFAULT_FEATURE_FLAGS
from django.db.models import Count, Avg, Q
from listings.models import Listing
from reviews.models import Review
from catalog.models import Category, Product
from stores.models import Store

def home(request):
    # Öne çıkan kategoriler (en çok ilana sahip olanlar)
    featured_categories = Category.objects.annotate(
        listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
    ).filter(listing_count__gt=0).order_by('-listing_count')[:6]

    # Son eklenen ilanlar
    recent_listings = Listing.objects.filter(is_active=True).select_related(
        'store', 'product', 'product__category'
    ).prefetch_related('images')[:8]

    # İstatistikler
    stats = {
        'total_listings': Listing.objects.filter(is_active=True).count(),
        'total_stores': Store.objects.filter(is_active=True).count(),
        'total_categories': Category.objects.annotate(
            listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
        ).filter(listing_count__gt=0).count(),
    }

    # Doğrulanmış mağazalar
    verified_stores = Store.objects.filter(is_verified=True, is_active=True)[:4]

    context = {
        "featured_categories": featured_categories,
        "recent_listings": recent_listings,
        "stats": stats,
        "verified_stores": verified_stores,
    }
    return render(request, "home.html", context)

def marketplace(request):
    from catalog.filters import ListingFilter
    import os
    from core import DEFAULT_FEATURE_FLAGS
    
    def _ff(name: str) -> bool:
        default = DEFAULT_FEATURE_FLAGS.get(name, False)
        raw = os.environ.get(name)
        return default if raw is None else raw.lower() in ("1", "true", "yes")
    
    # Base queryset with optimizations
    listings = Listing.objects.filter(is_active=True).select_related(
        'store', 'product', 'product__category'
    ).prefetch_related('images', 'reviews')
    
    # Apply django-filter
    filter_instance = ListingFilter(request.GET, queryset=listings)
    listings = filter_instance.qs
    
    # Get categories for sidebar (only main categories with listings)
    categories = Category.objects.filter(
        parent__isnull=True
    ).annotate(
        listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
    ).filter(listing_count__gt=0).order_by('name')

    # Additional filters (Search V1 - flag based)
    brand = request.GET.get('brand')
    rating_min = request.GET.get('rating_min')

    if _ff('FEATURE_SEARCH_V1'):
        if brand:
            listings = listings.filter(product__brand__icontains=brand)
        if rating_min:
            try:
                rating_threshold = float(rating_min)
                listings = listings.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=rating_threshold)
            except ValueError:
                pass

    # Sıralama
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        listings = listings.order_by('price')
    elif sort_by == 'price_high':
        listings = listings.order_by('-price')
    elif sort_by == 'oldest':
        listings = listings.order_by('created_at')
    elif sort_by == 'popular':
        listings = listings.annotate(
            review_count=Count('reviews')
        ).order_by('-review_count', '-created_at')
    elif sort_by == 'rating_high' and _ff('FEATURE_SEARCH_V1'):
        listings = listings.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating', '-created_at')
    else:  # newest
        listings = listings.order_by('-created_at')

    # Sayfalama
    from django.core.paginator import Paginator
    paginator = Paginator(listings, 20)  # Sayfa başına 20 öğe
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get current category from filter
    current_category = None
    category_id = request.GET.get('category')
    if category_id:
        try:
            current_category = Category.objects.get(id=category_id)
        except (Category.DoesNotExist, ValueError):
            pass

    context = {
        'page_obj': page_obj,
        'listings': page_obj,  # Geriye uyumluluk için
        'categories': categories,
        'current_category': current_category,
        'filter': filter_instance,  # Django-filter instance for template
        'search_query': request.GET.get('search', ''),
        'sort_by': sort_by,
        'condition': request.GET.get('condition', ''),
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
    }

    # Brand facet seçenekleri (kategoriye göre) - Search V1
    if _ff('FEATURE_SEARCH_V1'):
        brand_options = []
        try:
            if current_category:
                brand_options = list(
                    Product.objects.filter(category=current_category)
                    .exclude(brand__isnull=True)
                    .exclude(brand__exact='')
                    .values_list('brand', flat=True)
                    .distinct()[:50]
                )
            else:
                brand_options = list(
                    Product.objects.exclude(brand__isnull=True)
                    .exclude(brand__exact='')
                    .values_list('brand', flat=True)
                    .distinct()[:50]
                )
        except Exception:
            brand_options = []
        context['brand_options'] = brand_options
        context['brand'] = brand
        context['rating_min'] = rating_min
    return render(request, "marketplace.html", context)

def listing_detail(request, listing_id):
    try:
        listing = Listing.objects.select_related('store', 'product').prefetch_related('images', 'reviews').get(id=listing_id, is_active=True)
    except Listing.DoesNotExist:
        from django.http import Http404
        raise Http404("İlan bulunamadı")
    
    # İlgili ilanlar
    related_listings = Listing.objects.filter(
        product__category=listing.product.category,
        is_active=True
    ).exclude(id=listing_id).select_related('store', 'product').prefetch_related('images')[:4]

    context = {
        'listing': listing,
        'related_listings': related_listings,
    }
    return render(request, "listings/listing_detail.html", context)

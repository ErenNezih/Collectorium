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
    """
    Ana sayfa view'ı - FAILSAFE mantıkla yazılmıştır.
    Veritabanı boş olsa bile ASLA çökmemelidir.
    """
    # FAILSAFE: Öne çıkan kategoriler - Tüm hataları yakala
    featured_categories = Category.objects.none()  # Default: boş queryset
    try:
        # Önce listing'e sahip kategorileri kontrol et
        featured_categories_with_listings = Category.objects.filter(
            parent__isnull=True
        ).annotate(
            listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
        ).filter(listing_count__gt=0).order_by('-listing_count')[:6]
        
        if featured_categories_with_listings.exists():
            featured_categories = featured_categories_with_listings
        else:
            # Listing'e sahip kategori yoksa, tüm ana kategorileri göster
            featured_categories = Category.objects.filter(parent__isnull=True).annotate(
                listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
            ).order_by('name')[:6]
    except Exception:
        # Herhangi bir hata durumunda boş queryset döndür
        featured_categories = Category.objects.none()

    # FAILSAFE: Son eklenen ilanlar
    recent_listings = Listing.objects.none()  # Default: boş queryset
    try:
        recent_listings = Listing.objects.filter(is_active=True).select_related(
            'store', 'product'
        ).prefetch_related('images')[:8]
    except Exception:
        recent_listings = Listing.objects.none()

    # FAILSAFE: İstatistikler - Her biri ayrı try-except içinde
    stats = {
        'total_listings': 0,
        'total_stores': 0,
        'total_categories': 0,
        'total_reviews': 0,
    }
    
    try:
        stats['total_listings'] = Listing.objects.filter(is_active=True).count()
    except Exception:
        stats['total_listings'] = 0
    
    try:
        stats['total_stores'] = Store.objects.filter(is_active=True).count()
    except Exception:
        stats['total_stores'] = 0
    
    try:
        stats['total_categories'] = Category.objects.filter(parent__isnull=True).count()
    except Exception:
        stats['total_categories'] = 0
    
    try:
        stats['total_reviews'] = Review.objects.count()
    except Exception:
        stats['total_reviews'] = 0

    # FAILSAFE: Doğrulanmış mağazalar
    verified_stores = Store.objects.none()  # Default: boş queryset
    try:
        verified_stores = Store.objects.filter(is_verified=True, is_active=True)[:4]
    except Exception:
        verified_stores = Store.objects.none()

    context = {
        "featured_categories": featured_categories,
        "recent_listings": recent_listings,
        "new_listings": recent_listings,  # Template uses 'new_listings'
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
    
    # FAILSAFE: Get categories for sidebar - Show all main categories even if no listings
    categories = Category.objects.none()  # Default: boş queryset
    try:
        # First try to get categories with listings
        categories_with_listings = Category.objects.filter(
            parent__isnull=True
        ).annotate(
            listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
        ).filter(listing_count__gt=0).order_by('name')
        
        if categories_with_listings.exists():
            categories = categories_with_listings
        else:
            # If no categories with listings, show all main categories
            categories = Category.objects.filter(
                parent__isnull=True
            ).annotate(
                listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
            ).order_by('name')
    except Exception:
        # On any error, return empty queryset
        categories = Category.objects.none()

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

    # FAILSAFE: Get current category from filter
    current_category = None
    category_id = request.GET.get('category')
    if category_id:
        try:
            current_category = Category.objects.get(id=category_id)
        except (Category.DoesNotExist, ValueError, Exception):
            # On any error, set to None
            current_category = None

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

# --- Statik Sayfalar ---

class AboutView(TemplateView):
    template_name = "pages/about.html"

class PrivacyPolicyView(TemplateView):
    template_name = "pages/privacy_policy.html"

class TermsOfServiceView(TemplateView):
    template_name = "pages/terms_of_service.html"

class ContactView(TemplateView):
    template_name = "pages/contact.html"

class SellerGuideView(TemplateView):
    template_name = "pages/seller_guide.html"

class CommissionsView(TemplateView):
    template_name = "pages/commissions.html"

class SecurityTipsView(TemplateView):
    template_name = "pages/security_tips.html"

class DeliveryAndReturnsView(TemplateView):
    template_name = "pages/delivery_and_returns.html"

class DistanceSalesContractView(TemplateView):
    template_name = "pages/distance_sales_contract.html"

class CookiePolicyView(TemplateView):
    template_name = "pages/privacy_policy.html"  # Çerez politikası gizlilik politikası ile aynı sayfada

class TrustCenterView(TemplateView):
    template_name = "pages/trust_center.html"

    def dispatch(self, request, *args, **kwargs):
        default = DEFAULT_FEATURE_FLAGS.get('FEATURE_TRUST_CENTER_P1', False)
        raw = os.environ.get('FEATURE_TRUST_CENTER_P1')
        enabled = default if raw is None else raw.lower() in ("1","true","yes")
        if not enabled:
            return HttpResponseForbidden("Bu özellik şu anda aktif değil.")
        return super().dispatch(request, *args, **kwargs)

# --- Custom Error Handlers ---

def handler403(request, exception):
    """Custom 403 Forbidden error handler"""
    return render(request, '403.html', status=403)

def handler404(request, exception):
    """Custom 404 Not Found error handler"""
    return render(request, '404.html', status=404)

def handler500(request):
    """Custom 500 Internal Server Error handler"""
    return render(request, '500.html', status=500)

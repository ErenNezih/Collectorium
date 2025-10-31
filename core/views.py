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
    
    # En yeni ilanlar
    new_listings = Listing.objects.filter(is_active=True).select_related(
        'store', 'product', 'product__category'
    ).prefetch_related('images').order_by('-created_at')[:8]
    
    # En çok yorum alan ilanlar
    popular_listings = Listing.objects.filter(is_active=True).annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).filter(review_count__gt=0).order_by('-review_count')[:8]
    
    # İstatistikler
    stats = {
        'total_listings': Listing.objects.filter(is_active=True).count(),
        'total_stores': Store.objects.filter(is_verified=True).count(),
        'total_categories': Category.objects.annotate(
            listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
        ).filter(listing_count__gt=0).count(),
        'total_reviews': Review.objects.count(),
    }
    
    # Doğrulanmış mağazalar
    verified_stores = Store.objects.filter(is_verified=True).order_by('-created_at')[:6]
    
    context = {
        "featured_categories": featured_categories,
        "new_listings": new_listings,
        "popular_listings": popular_listings,
        "stats": stats,
        "verified_stores": verified_stores,
    }
    return render(request, "home.html", context)

def marketplace(request):
    listings = Listing.objects.filter(is_active=True).select_related(
        'store', 'product', 'product__category'
    ).prefetch_related('images', 'reviews')
    categories = Category.objects.annotate(
        listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
    ).filter(listing_count__gt=0).order_by('name')

    # Filtreleme
    category_slug = request.GET.get('category')
    if category_slug:
        listings = listings.filter(product__category__slug=category_slug)

    search_query = request.GET.get('search')
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) |
            Q(product__name__icontains=search_query) |
            Q(product__brand__icontains=search_query) |
            Q(store__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Durum filtresi
    condition = request.GET.get('condition')
    if condition:
        listings = listings.filter(condition=condition)

    # Fiyat aralığı filtresi
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        listings = listings.filter(price__gte=min_price)
    if max_price:
        listings = listings.filter(price__lte=max_price)

    # Ek filtreler (Search V1 - flag ile)
    import os
    from core import DEFAULT_FEATURE_FLAGS

    def _ff(name: str) -> bool:
        default = DEFAULT_FEATURE_FLAGS.get(name, False)
        raw = os.environ.get(name)
        return default if raw is None else raw.lower() in ("1", "true", "yes")

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

    # Mevcut kategori nesnesini al
    current_category = None
    if category_slug:
        try:
            current_category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            pass

    context = {
        'page_obj': page_obj,
        'listings': page_obj,  # Geriye uyumluluk için
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query,
        'sort_by': sort_by,
        'condition': condition,
        'min_price': min_price,
        'max_price': max_price,
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
    ).exclude(id=listing.id).select_related('store', 'product').prefetch_related('images')[:4]
    
    context = {
        'listing': listing,
        'related_listings': related_listings,
    }
    return render(request, "listing_detail.html", context)

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


class TrustCenterView(TemplateView):
    template_name = "pages/trust_center.html"

    def dispatch(self, request, *args, **kwargs):
        default = DEFAULT_FEATURE_FLAGS.get('FEATURE_TRUST_CENTER_P1', False)
        raw = os.environ.get('FEATURE_TRUST_CENTER_P1')
        enabled = default if raw is None else raw.lower() in ("1","true","yes")
        if not enabled:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class DeliveryAndReturnsView(TemplateView):
    template_name = "pages/delivery_and_returns.html"

class DistanceSalesContractView(TemplateView):
    template_name = "pages/distance_sales_contract.html"

class CookiePolicyView(TemplateView):
    template_name = "pages/cookie_policy.html"

# --- Hata Handler View'ları ---

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def handler403(request, exception):
    return render(request, '403.html', status=403)

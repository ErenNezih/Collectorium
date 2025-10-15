from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Store
from listings.models import Listing


def stores_list(request):
    """Mağazalar listesi sayfası"""
    stores = Store.objects.filter(is_verified=True).annotate(
        listing_count=Count('listings', filter=Q(listings__is_active=True))
    ).order_by('-created_at')
    
    # Arama
    search_query = request.GET.get('search')
    if search_query:
        stores = stores.filter(
            Q(name__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Sayfalama
    paginator = Paginator(stores, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'stores': page_obj,
        'search_query': search_query,
    }
    return render(request, 'stores/stores_list.html', context)


def store_detail(request, slug):
    """Mağaza detay sayfası"""
    store = get_object_or_404(Store, slug=slug, is_verified=True)
    
    # Mağazanın ilanları
    listings = Listing.objects.filter(
        store=store,
        is_active=True
    ).select_related('product', 'product__category').prefetch_related('images').order_by('-created_at')
    
    # Sayfalama
    paginator = Paginator(listings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'store': store,
        'page_obj': page_obj,
        'listings': page_obj,
    }
    return render(request, 'stores/store_detail.html', context)

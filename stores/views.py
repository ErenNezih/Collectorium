from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Store
from listings.models import Listing
from django.db.models import Avg, Count


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
    
    # Store rating aggregate (flag controlled)
    from core import DEFAULT_FEATURE_FLAGS
    import os
    def _ff(name: str) -> bool:
        default = DEFAULT_FEATURE_FLAGS.get(name, False)
        raw = os.environ.get(name)
        return default if raw is None else raw.lower() in ("1", "true", "yes")

    if _ff('FEATURE_STORE_REVIEWS'):
        agg = store.listings.aggregate(avg=Avg('reviews__rating'), cnt=Count('reviews'))
        store.rating_avg = agg['avg'] or store.rating_avg
        store.rating_count = agg['cnt'] or store.rating_count

    context = {
        'store': store,
        'page_obj': page_obj,
        'listings': page_obj,
    }
    # Add policy if flag enabled
    if _ff('FEATURE_STORE_POLICIES'):
        context['policy'] = getattr(store, 'policy', None)
    return render(request, 'stores/store_detail.html', context)


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from core import DEFAULT_FEATURE_FLAGS
import os


def _ff(name: str) -> bool:
    default = DEFAULT_FEATURE_FLAGS.get(name, False)
    raw = os.environ.get(name)
    return default if raw is None else raw.lower() in ("1", "true", "yes")


@login_required
def seller_dashboard(request):
    if not _ff('FEATURE_SELLER_DASHBOARD_V1'):
        return HttpResponseForbidden()
    store = getattr(request.user, 'owned_stores', None)
    store = store.first() if store else None
    if not store:
        return HttpResponseForbidden()
    # Orders overview (read-only)
    from orders.models import OrderItem
    order_items = OrderItem.objects.filter(listing__store=store).select_related('order','listing').order_by('-order__created_at')[:50]
    # Listings overview
    my_listings = Listing.objects.filter(store=store).order_by('-created_at')[:50]
    # Messaging overview
    from messaging.models import Thread
    threads = Thread.objects.filter(seller=request.user).order_by('-last_message_at','-created_at')[:50]
    return render(request, 'stores/seller_dashboard.html', {
        'store': store,
        'order_items': order_items,
        'my_listings': my_listings,
        'threads': threads,
    })


@login_required
def store_policies_edit(request):
    if not _ff('FEATURE_STORE_POLICIES'):
        return HttpResponseForbidden()
    store = getattr(request.user, 'owned_stores', None)
    store = store.first() if store else None
    if not store:
        return HttpResponseForbidden()
    from .forms import StorePolicyForm
    policy = getattr(store, 'policy', None)
    if request.method == 'POST':
        form = StorePolicyForm(request.POST, instance=policy)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.store = store
            obj.save()
            from django.contrib import messages as djm
            djm.success(request, 'Mağaza politikaları güncellendi.')
            return redirect('stores:seller_dashboard')
    else:
        form = StorePolicyForm(instance=policy)
    return render(request, 'stores/store_policies_form.html', {'form': form, 'store': store})
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from listings.models import Listing
from .cart import Cart
from .forms import CartAddListingForm

@require_POST
def cart_add(request, listing_id):
    """
    Bir ilanı sepete eklemek için view.
    """
    cart = Cart(request)
    listing = get_object_or_404(Listing, id=listing_id)
    form = CartAddListingForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(listing=listing,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        messages.success(request, f'"{listing.title}" sepete eklendi.')
    return redirect('cart:cart_detail')


def cart_remove(request, listing_id):
    """
    Bir ilanı sepetten silmek için view.
    """
    cart = Cart(request)
    listing = get_object_or_404(Listing, id=listing_id)
    cart.remove(listing)
    messages.info(request, f'"{listing.title}" sepetten çıkarıldı.')
    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    Sepet detaylarını gösteren sayfa için view.
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddListingForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})

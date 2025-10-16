from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import AddressForm, AddressSelectionForm
from cart.cart import Cart
from accounts.models import Address
from moderation.models import Ban, RiskSignal
from django.conf import settings
from core import DEFAULT_FEATURE_FLAGS
import os

@login_required
def order_create(request):
    cart = Cart(request)
    if not cart:
        # Boş sepetle bu sayfaya gelinirse marketplace'e yönlendir.
        return redirect('marketplace')

    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # sitewide/purchase ban guard
        from core import DEFAULT_FEATURE_FLAGS
        import os
        def _ff(name: str) -> bool:
            default = DEFAULT_FEATURE_FLAGS.get(name, False)
            raw = os.environ.get(name)
            return default if raw is None else raw.lower() in ("1", "true", "yes")
        if _ff('FEATURE_BLOCKLIST_P1'):
            if Ban.objects.filter(user=request.user, active=True, scope__in=['purchase','sitewide']).exclude(expires_at__lt=timezone.now()).exists():
                messages.error(request, 'Hesabınız şu anda satın alma için kısıtlı.')
                return redirect('cart:cart_detail')
        # Formdan gelen veriye göre adres seçimi mi yeni adres mi kontrol et
        selected_address_id = request.POST.get('selected_address')
        
        if selected_address_id:
            # Mevcut adres seçildiyse
            shipping_address_obj = Address.objects.get(id=selected_address_id, user=request.user)
            address_form = AddressForm() # Formu boş tut
            selection_form = AddressSelectionForm(request.POST, user=request.user)
        else:
            # Yeni adres formu doldurulduysa
            address_form = AddressForm(request.POST)
            selection_form = AddressSelectionForm(user=request.user)
            if address_form.is_valid():
                # Yeni adresi kaydet ama veritabanına henüz işleme
                shipping_address_obj = address_form.save(commit=False)
                shipping_address_obj.user = request.user
                shipping_address_obj.save()
            else:
                # Form valid değilse, hata ile sayfayı yeniden render et
                return render(request, 'orders/checkout.html', {
                    'cart': cart, 
                    'selection_form': selection_form, 
                    'address_form': address_form
                })

        # Adres belirlendiğine göre siparişi oluştur
        order = Order.objects.create(
            buyer=request.user,
            shipping_address=f"{shipping_address_obj.full_address}, {shipping_address_obj.district}, {shipping_address_obj.city}",
            total=cart.get_total_price(),
            status='paid' # varsayılan; payments flag açıkken aşağıda pending'e alınır
        )
        
        order_items_to_create = []
        for item in cart:
            order_items_to_create.append(OrderItem(
                order=order,
                listing=item['listing'],
                price_snapshot=item['price'],
                quantity=item['quantity']
            ))
        
        OrderItem.objects.bulk_create(order_items_to_create)
        # Sepeti temizle
        cart.clear()

        # Payments sandbox flag açıksa sipariş durumunu pending yap ve ödeme akışına dallan
        from core import DEFAULT_FEATURE_FLAGS
        import os
        def _ff(name: str) -> bool:
            default = DEFAULT_FEATURE_FLAGS.get(name, False)
            raw = os.environ.get(name)
            return default if raw is None else raw.lower() in ("1", "true", "yes")

        if _ff("P0_FEATURES_ENABLED") and _ff("FEATURE_PAYMENTS_SANDBOX"):
            order.status = 'pending'
            order.save(update_fields=['status'])

        # Oluşturulan siparişin ID'sini session'a kaydet
        request.session['order_id'] = order.id

        # Payments sandbox flag açıksa ödeme akışına dallan
        def _ff(name: str) -> bool:
            default = DEFAULT_FEATURE_FLAGS.get(name, False)
            raw = os.environ.get(name)
            return default if raw is None else raw.lower() in ("1", "true", "yes")

        if _ff("P0_FEATURES_ENABLED") and _ff("FEATURE_PAYMENTS_SANDBOX"):
            return redirect('payments:start', order_id=order.id)
        # risk: first_order/high_amount
        if _ff('FEATURE_RISK_SIGNALS_P2'):
            total = float(order.total)
            if Order.objects.filter(buyer=request.user).exclude(id=order.id).count() == 0:
                RiskSignal.objects.create(entity_type='user', entity_id=request.user.id, type='first_order', severity='low', meta={'order_id': order.id})
            if total >= 10000:
                RiskSignal.objects.create(entity_type='order', entity_id=order.id, type='high_amount', severity='high', meta={'total': total})

        messages.success(request, f'Siparişiniz başarıyla oluşturuldu! Sipariş numaranız: #{order.id}')
        return redirect('orders:order_created')

    else:
        # GET request için
        selection_form = AddressSelectionForm(user=request.user)
        address_form = AddressForm()

    return render(request, 'orders/checkout.html', {
        'cart': cart, 
        'selection_form': selection_form, 
        'address_form': address_form
    })


def order_created(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id) if order_id else None
    return render(request, 'orders/order_created.html', {'order': order})

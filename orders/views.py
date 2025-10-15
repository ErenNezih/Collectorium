from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import AddressForm, AddressSelectionForm
from cart.cart import Cart
from accounts.models import Address

@login_required
def order_create(request):
    cart = Cart(request)
    if not cart:
        # Boş sepetle bu sayfaya gelinirse marketplace'e yönlendir.
        return redirect('marketplace')

    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
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
            status='paid' # Ödemenin başarılı olduğunu varsayıyoruz
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

        # Oluşturulan siparişin ID'sini session'a kaydet
        request.session['order_id'] = order.id
        
        messages.success(request, f'Siparişiniz başarıyla oluşturuldu! Sipariş numaranız: #{order.id}')
        
        # Teşekkür sayfasına yönlendir
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

from decimal import Decimal
from django.conf import settings
from listings.models import Listing

class Cart:
    def __init__(self, request):
        """
        Sepeti başlat.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Session'da boş bir sepet oluştur
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, listing, quantity=1, override_quantity=False):
        """
        Ürünü sepete ekle veya miktarını güncelle.
        """
        listing_id = str(listing.id)
        if listing_id not in self.cart:
            self.cart[listing_id] = {'quantity': 0, 'price': str(listing.price)}
        
        if override_quantity:
            self.cart[listing_id]['quantity'] = quantity
        else:
            self.cart[listing_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Session'ı "modified" olarak işaretle ve kaydet
        self.session.modified = True

    def remove(self, listing):
        """
        Ürünü sepetten kaldır.
        """
        listing_id = str(listing.id)
        if listing_id in self.cart:
            del self.cart[listing_id]
            self.save()

    def __iter__(self):
        """
        Sepetteki ürünler arasında döngü kur ve veritabanından
        ürün nesnelerini al.
        """
        listing_ids = self.cart.keys()
        # İlgili ürün nesnelerini al ve sepete ekle
        listings = Listing.objects.filter(id__in=listing_ids)
        cart = self.cart.copy()
        for listing in listings:
            cart[str(listing.id)]['listing'] = listing
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Sepetteki toplam ürün adedini (quantity) say.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Sepetin toplam tutarını hesapla.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Sepeti session'dan sil
        del self.session[settings.CART_SESSION_ID]
        self.save()
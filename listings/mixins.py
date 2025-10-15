from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Listing

class ListingOwnerRequiredMixin(UserPassesTestMixin):
    """
    Bu view'ı talep eden kullanıcının, URL'de belirtilen
    ilanın sahibi olduğunu doğrular.
    """
    def test_func(self):
        # URL'den gelen 'pk' (primary key) ile ilanı bul
        listing = get_object_or_404(Listing, pk=self.kwargs['pk'])
        
        # Giriş yapmış kullanıcının sahip olduğu ilk mağazanın,
        # ilanın ait olduğu mağaza ile aynı olup olmadığını kontrol et.
        user_store = self.request.user.owned_stores.first()
        return listing.store == user_store
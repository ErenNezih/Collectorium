from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class SellerRequiredMixin(UserPassesTestMixin):
    """Kullanıcının 'seller' rolüne sahip olduğunu ve bir mağazası olduğunu doğrular."""
    def test_func(self):
        # User modelinde owner alanı: owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stores')
        # Bu yüzden `self.request.user.owned_stores.exists()` daha doğru bir kontrol.
        return self.request.user.is_authenticated and self.request.user.role == 'seller' and self.request.user.owned_stores.exists()

    def handle_no_permission(self):
        # İzin verilmeyen kullanıcılar için bir mesaj gösterip ana sayfaya yönlendirebiliriz.
        return redirect('home')
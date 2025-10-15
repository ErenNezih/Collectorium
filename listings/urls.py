from django.urls import path
from .views import ListingCreateView, ListingUpdateView, ListingDeleteView

app_name = 'listings'

urlpatterns = [
    # Örnek: path('<slug:slug>/', ListingDetailView.as_view(), name='listing_detail'),
    path('new/', ListingCreateView.as_view(), name='listing_create'),
    path('<int:pk>/edit/', ListingUpdateView.as_view(), name='listing_edit'),
    path('<int:pk>/delete/', ListingDeleteView.as_view(), name='listing_delete'), # YENİ SATIR
    # Diğer ilan URL'leri buraya gelecek
]
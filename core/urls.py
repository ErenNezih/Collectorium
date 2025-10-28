from django.urls import path
from . import views, health
from .views import AboutView, PrivacyPolicyView, TermsOfServiceView, ContactView, SellerGuideView, TrustCenterView, DeliveryAndReturnsView, DistanceSalesContractView, CookiePolicyView

urlpatterns = [
    path("", views.home, name="home"),
    path("marketplace/", views.marketplace, name="marketplace"),
    path("listing/<int:listing_id>/", views.listing_detail, name="listing_detail"),
    
    # Health Check Endpoints
    path('healthz/', health.healthz, name='healthz'),
    path('health/readiness/', health.readiness, name='health_readiness'),
    path('health/liveness/', health.liveness, name='health_liveness'),
    
    # Statik Sayfalar
    path('hakkimizda/', AboutView.as_view(), name='about'),
    path('gizlilik-politikasi/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('cerez-politikasi/', CookiePolicyView.as_view(), name='cookie_policy'),
    path('kullanim-kosullari/', TermsOfServiceView.as_view(), name='terms_of_service'),
    path('kullanici-sozlesmesi/', TermsOfServiceView.as_view(), name='user_agreement'),  # Kullanıcı Sözleşmesi (Kullanım Koşulları ile aynı)
    path('iletisim/', ContactView.as_view(), name='contact'),
    path('satici-rehberi/', SellerGuideView.as_view(), name='seller_guide'),
    # Yeni Yasal Sayfalar
    path('teslimat-ve-iade/', DeliveryAndReturnsView.as_view(), name='delivery_and_returns'),
    path('mesafeli-satis-sozlesmesi/', DistanceSalesContractView.as_view(), name='distance_sales_contract'),
    # Güven Merkezi (flag kontrolü template tarafında yapılır)
    path('trust/', TrustCenterView.as_view(), name='trust_center'),
]

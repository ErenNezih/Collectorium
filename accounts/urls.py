from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('orders/', views.my_orders, name='my_orders'),
    path('reviews/', views.my_reviews, name='my_reviews'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('my-listings/', views.MyListingsView.as_view(), name='my_listings'),
    path('user/<str:username>/', views.UserDetailView.as_view(), name='user_detail'),
    
    # KEYSTONE OPERASYONU - Google Onboarding
    path('google/signup/complete/', views.google_onboarding_complete, name='google_onboarding_complete'),

    # Verified Seller / KYC (feature-flagged)
    path('seller/verify/apply/', views.verified_seller_apply, name='verified_seller_apply'),
    path('seller/verify/status/', views.verified_seller_status, name='verified_seller_status'),
]






from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.stores_list, name='stores_list'),
    path('<slug:slug>/', views.store_detail, name='store_detail'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/policies/', views.store_policies_edit, name='store_policies_edit'),
]


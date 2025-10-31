from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.categories_list, name='categories_list'),
    path('<slug:parent_slug>/', views.subcategory_list, name='subcategory_list'),  # Alt kategori reyonları
    path('<slug:slug>/detay/', views.category_detail, name='category_detail'),  # Kategori detay (marketplace'e yönlendirir)
]


from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.categories_list, name='categories_list'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
]


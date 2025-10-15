from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.stores_list, name='stores_list'),
    path('<slug:slug>/', views.store_detail, name='store_detail'),
]


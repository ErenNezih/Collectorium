from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.results, name='results'),
    path('map/', views.map_search, name='map'),
    path('saved/', views.saved_search_list, name='saved_list'),
    path('saved/create', views.saved_search_create, name='saved_create'),
    path('saved/<int:pk>/update', views.saved_search_update, name='saved_update'),
    path('saved/<int:pk>/delete', views.saved_search_delete, name='saved_delete'),
    path('compare/', views.compare, name='compare'),
    path('price-trends/<slug:category_slug>/', views.price_trends, name='price_trends'),
]



from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),
    path('listings/', include('listings.urls', namespace='listings')),
    path('account/', include('accounts.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('stores/', include('stores.urls', namespace='stores')),
    path('categories/', include('catalog.urls', namespace='catalog')),
    path('search/', include('search.urls', namespace='search')),
    path('m/', include('messaging.urls', namespace='messaging')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('mod/', include('moderation.urls', namespace='moderation')),
]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Hata Handler'ları (DEBUG=False olduğunda çalışır)
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
handler403 = 'core.views.handler403'

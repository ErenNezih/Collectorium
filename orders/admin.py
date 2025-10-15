from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price_snapshot',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'total', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('buyer__username', 'buyer__email', 'shipping_address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'listing', 'quantity', 'price_snapshot')
    list_filter = ('created_at',)
    search_fields = ('order__buyer__username', 'listing__title')
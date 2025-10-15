from django.contrib import admin
from .models import Listing, ListingImage


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary')


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'product', 'price', 'condition', 'stock', 'is_active', 'created_at')
    list_filter = ('condition', 'is_active', 'currency', 'created_at')
    search_fields = ('title', 'description', 'store__name', 'product__name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ListingImageInline]


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('listing__title', 'alt_text')
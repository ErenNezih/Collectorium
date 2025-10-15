from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('name', 'owner__username', 'owner__email')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
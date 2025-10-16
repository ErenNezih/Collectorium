from django.contrib import admin
from .models import SavedSearch, PricePoint


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "frequency", "active", "last_run_at", "created_at")
    search_fields = ("name", "user__username", "querystring")
    list_filter = ("frequency", "active", "created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(PricePoint)
class PricePointAdmin(admin.ModelAdmin):
    list_display = ("listing", "kind", "price", "currency", "at", "source")
    list_filter = ("kind", "currency", "at")
    search_fields = ("listing__title",)

# Register your models here.

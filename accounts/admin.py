from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from .models import Address

# Import allauth models to ensure they're registered in admin
# This is critical for AEGIS Operation - CEO needs to manage Google OAuth
try:
    from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
    # These are auto-registered by allauth, but we import them here
    # to ensure they're always visible in the admin panel
except ImportError:
    pass

User = get_user_model()

# Customize Site admin to make it more user-friendly for AEGIS Operation
class CustomSiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name', 'id')
    search_fields = ('domain', 'name')
    ordering = ('id',)

# Unregister the default Site admin and register our custom one
try:
    admin.site.unregister(Site)
except admin.sites.NotRegistered:
    pass
admin.site.register(Site, CustomSiteAdmin)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","email","role","store_name","is_staff","date_joined")
    search_fields = ("username","email","store_name","first_name","last_name")
    list_filter = ("role","is_staff","is_superuser","date_joined")
    readonly_fields = ("date_joined","last_login")
    fieldsets = (
        ('Temel Bilgiler', {'fields': ('username', 'email', 'first_name', 'last_name')}),
        ('Platform Rolü', {'fields': ('role', 'store_name')}),
        ('İletişim', {'fields': ('phone', 'birth_date')}),
        ('Yetkiler', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Tarihçe', {'fields': ('date_joined', 'last_login')}),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user","address_title","city","district","is_default","created_at")
    search_fields = ("user__username","user__email","city","district","full_address")
    list_filter = ("is_default","city","created_at")
    readonly_fields = ("created_at","updated_at")
    raw_id_fields = ("user",)

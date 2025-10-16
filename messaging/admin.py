from django.contrib import admin
from .models import Thread, ThreadMessage, Block


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("listing", "buyer", "seller", "is_open", "last_message_at", "created_at")
    list_filter = ("is_open", "created_at")
    search_fields = ("listing__title", "buyer__username", "seller__username")


@admin.register(ThreadMessage)
class ThreadMessageAdmin(admin.ModelAdmin):
    list_display = ("thread", "sender", "has_contact_violation", "is_reported", "created_at")
    list_filter = ("has_contact_violation", "is_reported", "created_at")
    search_fields = ("raw_text",)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("blocker", "blocked", "expires_at", "created_at")
    search_fields = ("blocker__username", "blocked__username")

# Register your models here.

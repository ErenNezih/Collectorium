from django.contrib import admin
from .models import Report, ModerationAction, RiskSignal, Ban
from django.contrib import messages
from listings.models import Listing
from messaging.models import ThreadMessage
from django.utils import timezone


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "target_type", "target_id", "reporter", "status", "created_at")
    list_filter = ("status", "target_type", "created_at")
    search_fields = ("target_type", "target_id", "reporter__username")
    actions = ["action_hide_listing", "action_delete_message", "action_warn_user", "action_close"]

    def _create_action(self, request, queryset, action_name, severity="low", notes=""):
        count = 0
        for rep in queryset:
            ModerationAction.objects.create(report=rep, action=action_name, severity=severity, notes=notes, actor=request.user)
            if action_name == "hide_listing" and rep.target_type == "listing":
                try:
                    li = Listing.objects.get(id=rep.target_id)
                    li.is_active = False
                    li.save(update_fields=["is_active"])
                except Listing.DoesNotExist:
                    pass
            if action_name == "delete_message" and rep.target_type == "message":
                try:
                    msg = ThreadMessage.objects.get(id=rep.target_id)
                    msg.delete()
                except ThreadMessage.DoesNotExist:
                    pass
            rep.status = "actioned"
            rep.save(update_fields=["status", "updated_at"])
            count += 1
        self.message_user(request, f"{count} rapor işlendi.")

    def action_hide_listing(self, request, queryset):
        self._create_action(request, queryset, "hide_listing", severity="high")

    def action_delete_message(self, request, queryset):
        self._create_action(request, queryset, "delete_message", severity="medium")

    def action_warn_user(self, request, queryset):
        self._create_action(request, queryset, "warn_user", severity="low")

    def action_close(self, request, queryset):
        for rep in queryset:
            ModerationAction.objects.create(report=rep, action="no_action", severity="low", actor=request.user)
            rep.status = "closed"
            rep.save(update_fields=["status", "updated_at"])
        self.message_user(request, f"{queryset.count()} rapor kapatıldı.")

    action_hide_listing.short_description = "İlanı gizle"
    action_delete_message.short_description = "Mesajı sil"
    action_warn_user.short_description = "Kullanıcıyı uyar"
    action_close.short_description = "Raporu kapat (No Action)"


@admin.register(ModerationAction)
class ModerationActionAdmin(admin.ModelAdmin):
    list_display = ("report", "action", "severity", "actor", "created_at")
    list_filter = ("action", "severity", "created_at")
    search_fields = ("notes",)


@admin.register(RiskSignal)
class RiskSignalAdmin(admin.ModelAdmin):
    list_display = ("entity_type", "entity_id", "type", "severity", "created_at")
    list_filter = ("type", "severity", "created_at")
    search_fields = ("entity_type", "entity_id")


@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    list_display = ("user", "scope", "active", "expires_at", "created_by", "created_at")
    list_filter = ("scope", "active", "created_at")
    search_fields = ("user__username", "reason")

# Register your models here.

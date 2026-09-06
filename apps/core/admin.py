from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import SiteSettings, User

admin.site.site_header = _("Alupan administration")
admin.site.site_title = _("Alupan")
admin.site.index_title = _("Content management")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (_("Profile"), {"fields": ("display_name", "phone")}),
    )
    list_display = ("username", "email", "display_name", "is_staff")
    search_fields = ("username", "email", "display_name")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request) -> bool:
        # Singleton: block the "Add" button once the row exists.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

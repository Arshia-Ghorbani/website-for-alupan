from django.contrib import admin

from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company", "kind", "status", "created_at")
    list_filter = ("status", "kind", "created_at")
    search_fields = ("full_name", "company", "email", "subject", "message")
    readonly_fields = ("created_at", "updated_at", "ip_address", "user_agent")
    list_editable = ("status",)
    date_hierarchy = "created_at"

    def has_add_permission(self, request) -> bool:
        return False  # inquiries only arrive from the public form

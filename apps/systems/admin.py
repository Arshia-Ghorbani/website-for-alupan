from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline

from .models import System, SystemCategory, SystemImage


class SystemImageInline(TranslationTabularInline):
    model = SystemImage
    extra = 1


@admin.register(SystemCategory)
class SystemCategoryAdmin(TabbedTranslationAdmin):
    list_display = ("name", "sort_order")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("sort_order",)


@admin.register(System)
class SystemAdmin(TabbedTranslationAdmin):
    list_display = ("name", "code", "category", "status", "is_thermal_break", "sort_order")
    list_filter = ("status", "category", "is_thermal_break")
    search_fields = ("name", "code", "summary")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SystemImageInline]
    date_hierarchy = "published_at"

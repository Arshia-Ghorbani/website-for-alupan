from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline

from .models import Project, ProjectImage, ProjectSector


class ProjectImageInline(TranslationTabularInline):
    model = ProjectImage
    extra = 1


@admin.register(ProjectSector)
class ProjectSectorAdmin(TabbedTranslationAdmin):
    list_display = ("name", "sort_order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(TabbedTranslationAdmin):
    list_display = ("title", "sector", "city", "completion_year", "status", "is_featured")
    list_filter = ("status", "sector", "is_featured", "completion_year")
    search_fields = ("title", "client", "architect", "city")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("systems_used",)
    inlines = [ProjectImageInline]

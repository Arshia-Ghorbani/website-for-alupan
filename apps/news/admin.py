from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Article, ArticleCategory


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(TabbedTranslationAdmin):
    list_display = ("name", "sort_order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(TabbedTranslationAdmin):
    list_display = ("title", "category", "author", "status", "published_at")
    list_filter = ("status", "category")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    filter_horizontal = ("related_systems",)

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

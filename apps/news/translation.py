from modeltranslation.translator import TranslationOptions, register

from .models import Article, ArticleCategory


@register(ArticleCategory)
class ArticleCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ("title", "excerpt", "body", "meta_title", "meta_description")

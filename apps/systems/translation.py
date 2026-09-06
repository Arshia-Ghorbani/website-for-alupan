from modeltranslation.translator import TranslationOptions, register

from .models import System, SystemCategory, SystemImage


@register(SystemCategory)
class SystemCategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description", "meta_title", "meta_description")


@register(System)
class SystemTranslationOptions(TranslationOptions):
    fields = ("name", "summary", "description", "glazing_thickness_mm",
              "meta_title", "meta_description")


@register(SystemImage)
class SystemImageTranslationOptions(TranslationOptions):
    fields = ("caption",)

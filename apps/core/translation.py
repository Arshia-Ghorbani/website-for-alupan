"""django-modeltranslation registrations for the core app."""

from modeltranslation.translator import TranslationOptions, register

from .models import SiteSettings


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ("company_name", "tagline", "address")

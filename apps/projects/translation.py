from modeltranslation.translator import TranslationOptions, register

from .models import Project, ProjectImage, ProjectSector


@register(ProjectSector)
class ProjectSectorTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ("title", "summary", "description", "client", "architect", "city",
              "country", "meta_title", "meta_description")


@register(ProjectImage)
class ProjectImageTranslationOptions(TranslationOptions):
    fields = ("caption",)

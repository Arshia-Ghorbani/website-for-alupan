from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    label = "core"
    verbose_name = _("Core")

    def ready(self) -> None:
        # Import signal handlers / checks here.
        from . import signals  # noqa: F401

"""Signal receivers for the core app.  Imported from CoreConfig.ready()."""

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SiteSettings


@receiver(post_save, sender=SiteSettings)
def clear_site_settings_cache(sender, instance, **kwargs) -> None:
    cache.delete("site_settings")

from django.conf import settings
from django.db import DatabaseError

from .models import SiteSettings


def site_settings(request):
    """Expose {{ site }} and {{ SITE_NAME }} to every template.

    Wrapped defensively: this runs on error pages too, and a 500 caused by the
    database must not turn into a second exception while rendering 500.html.
    """
    try:
        site = SiteSettings.load()
    except DatabaseError:
        site = None
    return {
        "site": site,
        "SITE_NAME": settings.SITE_NAME,
    }

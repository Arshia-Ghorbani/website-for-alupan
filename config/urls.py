from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from apps.core.sitemaps import SITEMAPS

# Non-translated URLs: anything that must not carry a /fa/ or /en/ prefix.
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path("health/", include("apps.core.urls_health")),
]

# Translated URLs: /fa/... and /en/...
urlpatterns += i18n_patterns(
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("apps.core.urls", namespace="core")),
    path("systems/", include("apps.systems.urls", namespace="systems")),
    path("projects/", include("apps.projects.urls", namespace="projects")),
    path("news/", include("apps.news.urls", namespace="news")),
    path("contact/", include("apps.contact.urls", namespace="contact")),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = "apps.core.views.bad_request"
handler403 = "apps.core.views.permission_denied"
handler404 = "apps.core.views.page_not_found"
handler500 = "apps.core.views.server_error"

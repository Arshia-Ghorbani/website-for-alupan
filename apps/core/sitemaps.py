"""Central sitemap registry.  Each app contributes its own class."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.news.sitemaps import ArticleSitemap
from apps.projects.sitemaps import ProjectSitemap
from apps.systems.sitemaps import SystemSitemap


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"
    i18n = True

    def items(self):
        return ["core:home", "core:about", "contact:contact"]

    def location(self, item):
        return reverse(item)


SITEMAPS = {
    "static": StaticViewSitemap,
    "systems": SystemSitemap,
    "projects": ProjectSitemap,
    "news": ArticleSitemap,
}

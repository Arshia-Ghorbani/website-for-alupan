from django.contrib.sitemaps import Sitemap

from .models import Project


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    i18n = True

    def items(self):
        return Project.objects.published()

    def lastmod(self, obj):
        return obj.updated_at

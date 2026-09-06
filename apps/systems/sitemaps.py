from django.contrib.sitemaps import Sitemap

from .models import System


class SystemSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9
    i18n = True

    def items(self):
        return System.objects.published()

    def lastmod(self, obj):
        return obj.updated_at

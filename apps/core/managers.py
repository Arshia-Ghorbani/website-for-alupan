"""Reusable managers.  Kept separate from models.py so imports stay cheap."""

from django.db import models


class SlugLookupMixin:
    """`Model.objects.by_slug("curtain-wall")` without repeating the filter."""

    def by_slug(self, slug: str):
        return self.get(slug=slug)


class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

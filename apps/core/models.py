"""
Abstract building blocks every other app inherits from, plus the two concrete
site-wide models (custom User and the SiteSettings singleton).

Keeping these here means `systems`, `projects` and `news` share one definition
of "published", "SEO fields" and "timestamps" instead of re-inventing them.
"""

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# ---------------------------------------------------------------------------
# Abstract bases
# ---------------------------------------------------------------------------
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            status=PublishableModel.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        )

    def draft(self):
        return self.filter(status=PublishableModel.Status.DRAFT)


class PublishableModel(TimeStampedModel):
    """Editorial workflow: draft -> published, with a scheduled publish date."""

    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        PUBLISHED = "published", _("Published")
        ARCHIVED = "archived", _("Archived")

    status = models.CharField(
        _("status"),
        max_length=16,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(_("published at"), null=True, blank=True, db_index=True)

    objects = PublishedQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_live(self) -> bool:
        return (
            self.status == self.Status.PUBLISHED
            and self.published_at is not None
            and self.published_at <= timezone.now()
        )


class SEOModel(models.Model):
    """Per-page meta tags.  Translated by modeltranslation."""

    meta_title = models.CharField(_("meta title"), max_length=70, blank=True)
    meta_description = models.CharField(_("meta description"), max_length=160, blank=True)
    og_image = models.ImageField(_("social share image"), upload_to="seo/", blank=True)
    noindex = models.BooleanField(_("hide from search engines"), default=False)

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """Manual ordering for anything an editor drags around in the admin."""

    sort_order = models.PositiveIntegerField(_("sort order"), default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ["sort_order"]


# ---------------------------------------------------------------------------
# Concrete models
# ---------------------------------------------------------------------------
class User(AbstractUser):
    """
    Custom user, swapped in before the first migration.

    Adding a field to this later is a one-line migration; swapping AUTH_USER_MODEL
    after the fact is a multi-day data migration — which is why it exists on day one.
    """

    display_name = models.CharField(_("display name"), max_length=150, blank=True)
    phone = models.CharField(_("phone"), max_length=32, blank=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.display_name or self.get_username()


class SiteSettings(TimeStampedModel):
    """
    Singleton row holding the values marketing wants to edit without a deploy:
    head-office address, phone numbers, social links, footer blurb.
    """

    company_name = models.CharField(_("company name"), max_length=120, default="Alupan")
    tagline = models.CharField(_("tagline"), max_length=200, blank=True)
    address = models.TextField(_("address"), blank=True)
    phone = models.CharField(_("phone"), max_length=64, blank=True)
    fax = models.CharField(_("fax"), max_length=64, blank=True)
    email = models.EmailField(_("email"), blank=True)
    linkedin_url = models.URLField(_("LinkedIn"), blank=True)
    instagram_url = models.URLField(_("Instagram"), blank=True)
    catalog = models.FileField(_("general catalog (PDF)"), upload_to="catalogs/", blank=True)
    google_analytics_id = models.CharField(_("Google Analytics ID"), max_length=32, blank=True)

    class Meta:
        verbose_name = _("site settings")
        verbose_name_plural = _("site settings")

    def __str__(self) -> str:
        return str(_("Site settings"))

    def clean(self):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError(_("Only one SiteSettings instance is allowed."))

    def save(self, *args, **kwargs):
        self.pk = self.pk or 1  # force a single row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> "SiteSettings":
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj

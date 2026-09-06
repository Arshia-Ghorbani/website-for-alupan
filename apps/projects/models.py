"""Built references — the portfolio that wins B2B tenders."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import OrderedModel, PublishableModel, SEOModel


class ProjectSector(OrderedModel):
    """Commercial / Residential / Hospitality / Industrial ..."""

    name = models.CharField(_("name"), max_length=120)
    slug = models.SlugField(_("slug"), max_length=140, unique=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _("sector")
        verbose_name_plural = _("sectors")

    def __str__(self) -> str:
        return self.name


class Project(PublishableModel, OrderedModel, SEOModel):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=220, unique=True)
    sector = models.ForeignKey(
        ProjectSector,
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name=_("sector"),
    )
    client = models.CharField(_("client"), max_length=200, blank=True)
    architect = models.CharField(_("architect"), max_length=200, blank=True)
    city = models.CharField(_("city"), max_length=120, blank=True)
    country = models.CharField(_("country"), max_length=120, blank=True, default="Iran")
    completion_year = models.PositiveSmallIntegerField(_("completion year"), null=True, blank=True)
    facade_area_sqm = models.PositiveIntegerField(_("facade area (m²)"), null=True, blank=True)

    summary = models.CharField(_("summary"), max_length=300, blank=True)
    description = models.TextField(_("description"), blank=True)

    systems_used = models.ManyToManyField(
        "systems.System",
        related_name="projects",
        blank=True,
        verbose_name=_("systems used"),
    )

    cover_image = models.ImageField(_("cover image"), upload_to="projects/", blank=True)
    is_featured = models.BooleanField(_("featured on homepage"), default=False, db_index=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ["-completion_year", "sort_order"]
        indexes = [models.Index(fields=["status", "is_featured"])]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("projects:detail", kwargs={"slug": self.slug})

    @property
    def location(self) -> str:
        return ", ".join(part for part in (self.city, self.country) if part)


class ProjectImage(OrderedModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images", verbose_name=_("project")
    )
    image = models.ImageField(_("image"), upload_to="projects/gallery/")
    caption = models.CharField(_("caption"), max_length=200, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _("project image")
        verbose_name_plural = _("project images")

    def __str__(self) -> str:
        return self.caption or f"{self.project} #{self.pk}"

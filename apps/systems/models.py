"""
The product catalogue: the aluminium *systems* Alupan manufactures
(curtain wall, thermal-break windows, sliding doors, louvres, ...).

This is the app the rest of the site points at: projects reference the systems
they were built with, and news articles can be tagged to a system.
"""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import OrderedModel, PublishableModel, SEOModel


class SystemCategory(OrderedModel, SEOModel):
    """Top-level grouping, e.g. Facade Systems / Window Systems / Door Systems."""

    name = models.CharField(_("name"), max_length=120)
    slug = models.SlugField(_("slug"), max_length=140, unique=True)
    description = models.TextField(_("description"), blank=True)
    icon = models.FileField(_("icon (SVG)"), upload_to="systems/icons/", blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _("system category")
        verbose_name_plural = _("system categories")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("systems:category", kwargs={"slug": self.slug})


class System(PublishableModel, OrderedModel, SEOModel):
    category = models.ForeignKey(
        SystemCategory,
        on_delete=models.PROTECT,
        related_name="systems",
        verbose_name=_("category"),
    )
    name = models.CharField(_("name"), max_length=160)
    slug = models.SlugField(_("slug"), max_length=180, unique=True)
    code = models.CharField(_("series code"), max_length=32, blank=True, help_text=_("e.g. AP-70TB"))
    summary = models.CharField(_("summary"), max_length=300, blank=True)
    description = models.TextField(_("description"), blank=True)

    # Technical data an engineer or architect actually filters on.
    thermal_transmittance = models.DecimalField(
        _("Uf value (W/m²K)"), max_digits=5, decimal_places=2, null=True, blank=True
    )
    max_span_mm = models.PositiveIntegerField(_("max span (mm)"), null=True, blank=True)
    glazing_thickness_mm = models.CharField(_("glazing thickness (mm)"), max_length=64, blank=True)
    is_thermal_break = models.BooleanField(_("thermal break"), default=False)

    hero_image = models.ImageField(_("hero image"), upload_to="systems/", blank=True)
    datasheet = models.FileField(_("technical datasheet (PDF)"), upload_to="systems/datasheets/", blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _("system")
        verbose_name_plural = _("systems")
        indexes = [models.Index(fields=["status", "published_at"])]

    def __str__(self) -> str:
        return f"{self.code} — {self.name}" if self.code else self.name

    def get_absolute_url(self) -> str:
        return reverse("systems:detail", kwargs={"slug": self.slug})


class SystemImage(OrderedModel):
    system = models.ForeignKey(
        System, on_delete=models.CASCADE, related_name="images", verbose_name=_("system")
    )
    image = models.ImageField(_("image"), upload_to="systems/gallery/")
    caption = models.CharField(_("caption"), max_length=200, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _("system image")
        verbose_name_plural = _("system images")

    def __str__(self) -> str:
        return self.caption or f"{self.system} #{self.pk}"

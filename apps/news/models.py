"""Company news, trade-fair announcements and technical articles."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import OrderedModel, PublishableModel, SEOModel


class ArticleCategory(OrderedModel):
    name = models.CharField(_("name"), max_length=120)
    slug = models.SlugField(_("slug"), max_length=140, unique=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _("article category")
        verbose_name_plural = _("article categories")

    def __str__(self) -> str:
        return self.name


class Article(PublishableModel, SEOModel):
    title = models.CharField(_("title"), max_length=220)
    slug = models.SlugField(_("slug"), max_length=240, unique=True)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name=_("category"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name=_("author"),
    )
    excerpt = models.CharField(_("excerpt"), max_length=300, blank=True)
    body = models.TextField(_("body"))
    cover_image = models.ImageField(_("cover image"), upload_to="news/", blank=True)
    related_systems = models.ManyToManyField(
        "systems.System", related_name="articles", blank=True, verbose_name=_("related systems")
    )
    view_count = models.PositiveIntegerField(_("views"), default=0, editable=False)

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")
        ordering = ["-published_at"]
        indexes = [models.Index(fields=["status", "-published_at"])]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("news:detail", kwargs={"slug": self.slug})

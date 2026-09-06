"""Inbound sales enquiries — the only write path the public has into the database."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Inquiry(TimeStampedModel):
    class Kind(models.TextChoices):
        GENERAL = "general", _("General enquiry")
        QUOTE = "quote", _("Request for quotation")
        TECHNICAL = "technical", _("Technical support")
        PARTNERSHIP = "partnership", _("Partnership / dealership")

    class Status(models.TextChoices):
        NEW = "new", _("New")
        IN_PROGRESS = "in_progress", _("In progress")
        CLOSED = "closed", _("Closed")

    kind = models.CharField(_("type"), max_length=20, choices=Kind.choices, default=Kind.GENERAL)
    full_name = models.CharField(_("full name"), max_length=150)
    company = models.CharField(_("company"), max_length=200, blank=True)
    email = models.EmailField(_("email"))
    phone = models.CharField(_("phone"), max_length=32, blank=True)
    subject = models.CharField(_("subject"), max_length=200, blank=True)
    message = models.TextField(_("message"))
    related_system = models.ForeignKey(
        "systems.System",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inquiries",
        verbose_name=_("related system"),
    )
    attachment = models.FileField(_("attachment"), upload_to="inquiries/%Y/%m/", blank=True)

    status = models.CharField(
        _("status"), max_length=20, choices=Status.choices, default=Status.NEW, db_index=True
    )
    internal_notes = models.TextField(_("internal notes"), blank=True)

    # Anti-spam / audit trail
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)
    user_agent = models.CharField(_("user agent"), max_length=300, blank=True)

    class Meta:
        verbose_name = _("inquiry")
        verbose_name_plural = _("inquiries")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.full_name} — {self.get_kind_display()}"

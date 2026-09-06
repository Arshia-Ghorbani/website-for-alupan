"""Celery tasks.  Sending mail inline would block the request on a slow SMTP host."""

import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_inquiry_notification(self, inquiry_id: int) -> None:
    from .models import Inquiry

    try:
        inquiry = Inquiry.objects.select_related("related_system").get(pk=inquiry_id)
    except Inquiry.DoesNotExist:
        logger.warning("Inquiry %s vanished before notification", inquiry_id)
        return

    recipients = settings.SALES_NOTIFICATION_EMAILS
    if not recipients:
        logger.warning("SALES_NOTIFICATION_EMAILS is empty; skipping notification")
        return

    body = render_to_string("contact/email/inquiry_notification.txt", {"inquiry": inquiry})
    message = EmailMultiAlternatives(
        subject=f"New {inquiry.get_kind_display()} — {inquiry.full_name}",
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
        reply_to=[inquiry.email],
    )
    try:
        message.send(fail_silently=False)
    except Exception as exc:  # noqa: BLE001
        raise self.retry(exc=exc)


@shared_task
def send_inquiry_acknowledgement(inquiry_id: int) -> None:
    from .models import Inquiry

    inquiry = Inquiry.objects.filter(pk=inquiry_id).first()
    if not inquiry:
        return
    body = render_to_string("contact/email/inquiry_acknowledgement.txt", {"inquiry": inquiry})
    EmailMultiAlternatives(
        subject="Alupan — we received your enquiry",
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[inquiry.email],
    ).send(fail_silently=True)

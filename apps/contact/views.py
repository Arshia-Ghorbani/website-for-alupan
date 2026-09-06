from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from .forms import InquiryForm
from .models import Inquiry
from .tasks import send_inquiry_acknowledgement, send_inquiry_notification


class ContactView(CreateView):
    model = Inquiry
    form_class = InquiryForm
    template_name = "contact/contact.html"
    success_url = reverse_lazy("contact:thanks")

    def form_valid(self, form):
        form.instance.ip_address = self._client_ip()
        form.instance.user_agent = self.request.META.get("HTTP_USER_AGENT", "")[:300]
        response = super().form_valid(form)
        # Queued, not sent inline — the visitor gets an instant response.
        send_inquiry_notification.delay(self.object.pk)
        send_inquiry_acknowledgement.delay(self.object.pk)
        messages.success(self.request, _("Thank you — our team will be in touch shortly."))
        return response

    def _client_ip(self) -> str | None:
        forwarded = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return self.request.META.get("REMOTE_ADDR")

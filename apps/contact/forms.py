from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Inquiry


class InquiryForm(forms.ModelForm):
    # Hidden field bots fill in and humans never see.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Inquiry
        fields = [
            "kind", "full_name", "company", "email", "phone",
            "subject", "message", "related_system", "attachment",
        ]

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError(_("Spam detected."))
        return ""

    def clean_attachment(self):
        f = self.cleaned_data.get("attachment")
        if f and f.size > 5 * 1024 * 1024:
            raise forms.ValidationError(_("Attachments must be smaller than 5 MB."))
        return f

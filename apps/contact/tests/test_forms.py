import pytest

from apps.contact.forms import InquiryForm

VALID = {
    "kind": "quote",
    "full_name": "Sara Ahmadi",
    "email": "sara@example.com",
    "message": "Please quote 400 m2 of curtain wall.",
}


@pytest.mark.django_db
def test_valid_inquiry_is_accepted():
    assert InquiryForm(data=VALID).is_valid()


@pytest.mark.django_db
def test_honeypot_rejects_bots():
    form = InquiryForm(data={**VALID, "website": "http://spam.example"})
    assert not form.is_valid()
    assert "website" in form.errors

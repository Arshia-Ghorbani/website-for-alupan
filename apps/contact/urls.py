from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "contact"

urlpatterns = [
    path("", views.ContactView.as_view(), name="contact"),
    path("thanks/", TemplateView.as_view(template_name="contact/thanks.html"), name="thanks"),
]

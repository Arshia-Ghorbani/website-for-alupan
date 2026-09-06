from django.urls import path

from . import views

urlpatterns = [
    path("live/", views.healthz, name="healthz"),
    path("ready/", views.readyz, name="readyz"),
]

from django.urls import path

from . import views

app_name = "systems"

urlpatterns = [
    path("", views.SystemListView.as_view(), name="list"),
    path("category/<slug:slug>/", views.SystemCategoryView.as_view(), name="category"),
    path("<slug:slug>/", views.SystemDetailView.as_view(), name="detail"),
]

"""URL configuration."""
from django.urls import path
from testapp import views

urlpatterns = (
    path("noauth", views.anonymous_view, name="noauth"),
    path("auth", views.authenticated_view, name="auth"),
)

"""URL configuration."""
from django.contrib import admin
from django.urls import path
from testapp import views

urlpatterns = (
    path("login_required/", views.login_required_view, name="django_login_required"),
    path("admin/", admin.site.urls),
)

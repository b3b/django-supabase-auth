"""URL configuration."""
from django.contrib import admin
from django.urls import path
from testapp import views

urlpatterns = (
    path("session/", views.login_with_jwt, name="login_with_jwt"),
    path("admin/", admin.site.urls),
)

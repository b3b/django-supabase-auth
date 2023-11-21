"""URL configuration."""
from django.urls import path
from testapp import views

urlpatterns = (
    path("", views.SignInView.as_view(), name="supabase_signin"),
    path("noauth", views.anonymous_view, name="noauth"),
    path("auth", views.authenticated_view, name="auth"),
)

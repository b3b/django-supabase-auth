"""Django application configuration for the 'supa_auth' app."""
from django.apps import AppConfig


class SupaAuthConfig(AppConfig):
    """Application configuration."""

    name = "supa_auth"
    verbose_name = "Django Supabase authentication"

    def ready(self):
        from . import signals  # NOQA pylint: disable=unused-import

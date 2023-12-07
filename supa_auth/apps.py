"""Django application configuration for the 'supa_auth' app."""
from django.apps import AppConfig


class SupaAuthConfig(AppConfig):
    """Application configuration."""

    name = "supa_auth"
    verbose_name = "Django Supabase authentication"
    default = True

    def ready(self):
        """Sets up necessary signals when the application is ready."""
        from . import signals  # NOQA pylint: disable=unused-import


class NoModels(SupaAuthConfig):
    """Application configuration without the `supa_auth` models and migrations.

    This class represents a configuration option that excludes 'supa_auth'
    models and migrations from the application when using the original
    Django User model.

    Should be used in settings as:
        INSTALLED_APPS= {... 'supa_auth.apps.NoModels', ... }
    """

    name = "supa_auth.__init__"  # avoid triggering import of 'models.py'
    default = False

    def get_models(self, include_auto_created=False, include_swapped=False):
        """Returns an empty generator as configuration should not include any models."""
        yield from ()

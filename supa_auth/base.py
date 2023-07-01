"""supa_auth.base"""
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.postgresql.base import (
    DatabaseWrapper as PostgresqlDatabaseWrapper,
)

from . import settings as app_settings
from .client import DatabaseClient


class DatabaseWrapper(PostgresqlDatabaseWrapper):
    """A custom database wrapper for Supabase PostgreSQL connections.

    This wrapper sets appropriate default values for connection settings
    and ensures that required settings are present.
    """

    client_class = DatabaseClient
    _required_settings = ("HOST", "PASSWORD")
    _always_set_settings = (
        "NAME",
        "USER",
        "PASSWORD",
        "HOST",
        "PORT",
        "CONN_MAX_AGE",
        "CONN_HEALTH_CHECKS",
    )
    _allowed_sslmode = ("require", "verify-ca", "verify-full")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_settings_defaults()

    @property
    def _defaults(self) -> dict:
        """Default settings."""
        return {
            "PORT": "5432",
            "NAME": "postgres",
            "USER": "postgres",
            "CONN_MAX_AGE": app_settings.DEFAULT_CONN_MAX_AGE,
            "CONN_HEALTH_CHECKS": True,
        }

    @property
    def _default_options(self) -> dict:
        """Extra parameters to use when connecting to the database."""
        django_schema = self.settings_dict["SCHEMA"]
        return {
            "options": (
                f"-c search_path={django_schema},public,auth,extensions "
                f"-c tcp_keepalives_idle={app_settings.DEFAULT_KEEPALIVES_IDLE}"
            )
        }

    def _set_settings_defaults(self):
        """Set settings default values."""
        settings_dict = self.settings_dict

        settings_dict.setdefault("SCHEMA", app_settings.DEFAULT_SCHEMA)

        for key in self._always_set_settings:
            if not settings_dict.get(key, None):
                settings_dict.pop(key, None)

        missed_settings = set(self._required_settings) - set(settings_dict)
        if missed_settings:
            missing_setting = list(missed_settings)[0]
            raise ImproperlyConfigured(
                f"settings.DATABASES is improperly configured. "
                f"Please supply the setting: {missing_setting}."
            )

        sslmode = settings_dict.get("OPTIONS", {}).get("sslmode", None)
        if sslmode not in self._allowed_sslmode:
            raise ImproperlyConfigured(
                f"settings.DATABASES is improperly configured. "
                f"Please explicitly set OPTIONS['sslmode'] "
                f"to one of: {self._allowed_sslmode}."
            )

        self.settings_dict = self._defaults | settings_dict
        self.settings_dict["OPTIONS"] = self._default_options | self.settings_dict.get(
            "OPTIONS", {}
        )

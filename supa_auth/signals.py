"""supa_auth.signals"""
from typing import Any

from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.signals import connection_created
from django.db.models.signals import pre_migrate
from django.dispatch import receiver


@receiver(pre_migrate)
def create_schemas(sender, app_config, **kwargs):  # pylint: disable=unused-argument
    """Create database schemas before migrations are executed."""
    for connection in connections.all():
        backend_settings = connection.settings_dict
        if backend_settings["ENGINE"] == "supa_auth":
            with connection.cursor() as cursor:
                for schema_name in "auth", backend_settings["SCHEMA"]:
                    cursor.execute(f"create schema if not exists {schema_name};")


@receiver(connection_created)
def set_search_path(connection: BaseDatabaseWrapper, **kwargs: Any):
    """
    Set the search path for the database connection to prioritize the
    Django app SCHEMA over other Supabase schemas.
    """
    if connection.settings_dict["ENGINE"] == "supa_auth":
        django_schema = connection.settings_dict["SCHEMA"]
        with connection.cursor() as cursor:
            cursor.execute(
                f"SET search_path = {django_schema}, public, auth, extensions;"
            )

"""supa_auth.signals"""
from django.db import connections
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

# pylint: disable=unused-argument
import pytest
from django.core.exceptions import ImproperlyConfigured
from django.db import connection

from supa_auth.base import DatabaseWrapper


@pytest.fixture
def valid_settings():
    return {
        "ENGINE": "supa_auth",
        "HOST": "host",
        "PASSWORD": "pass",
        "OPTIONS": {"sslmode": "require"},
    }


def test_default_options_set(valid_settings):
    backend = DatabaseWrapper(valid_settings)
    backend_settings = backend.settings_dict
    assert backend_settings["HOST"] == "host"
    assert backend_settings["PASSWORD"] == "pass"
    assert backend_settings["SCHEMA"] == "django"
    assert "search_path" in backend_settings["OPTIONS"]["options"]


def test_setting_missed():
    with pytest.raises(ImproperlyConfigured, match=".*supply the setting.*"):
        DatabaseWrapper(
            {
                "ENGINE": "supa_auth",
                "HOST": "test",
            }
        )


def test_custom_schema_set(valid_settings):
    backend = DatabaseWrapper(
        {
            **valid_settings,
            "SCHEMA": "custom",
        }
    )
    backend_settings = backend.settings_dict
    assert backend_settings["SCHEMA"] == "custom"


def test_custom_options_added(valid_settings):
    backend = DatabaseWrapper(
        {
            **valid_settings,
            "OPTIONS": {
                "sslmode": "verify-full",
                "sslrootcert": "/etc/ssl/certs/prod-ca-2021.crt",
            },
        }
    )
    backend_settings = backend.settings_dict
    assert "sslrootcert" in backend_settings["OPTIONS"]
    assert "search_path" in backend_settings["OPTIONS"]["options"]


def test_options_replaced(valid_settings):
    backend = DatabaseWrapper(
        {**valid_settings, "OPTIONS": {"sslmode": "require", "options": "custom"}}
    )
    backend_settings = backend.settings_dict
    assert backend_settings["OPTIONS"]["options"] == "custom"


def test_connected_to_postgresql(db):
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        assert result[0].startswith("PostgreSQL")


def test_search_path_set(db):
    with connection.cursor() as cursor:
        cursor.execute("show search_path;")
        result = cursor.fetchone()
        assert result[0] == "django,public,auth,extensions"


def test_migrations_table_created_in_django_schema(db):
    with connection.cursor() as cursor:
        cursor.execute(
            (
                "select table_schema from information_schema.tables "
                "where table_name='django_migrations';"
            )
        )
        result = cursor.fetchone()
        assert result[0] == "django"

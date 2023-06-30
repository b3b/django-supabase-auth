from django.conf import settings

from .fixtures import *  # noqa


def pytest_configure():
    settings.configure(
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
        },
        SECRET_KEY="test",
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "rest_framework",
        ),
        SIMPLE_JWT={
            "JTI_CLAIM": None,
            "TOKEN_TYPE_CLAIM": None,
            "USER_ID_CLAIM": "sub",
            "SIGNING_KEY": "test",
            "VERIFYING_KEY": "test",
        },
    )

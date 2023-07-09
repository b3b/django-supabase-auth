from django.conf import settings
from environs import Env

from .fixtures import *  # noqa

env = Env()
env.read_env()


def pytest_configure():
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "supa_auth",
                "HOST": env("SUPABASE_HOST"),
                "PASSWORD": env("SUPABASE_PASSWORD"),
                "OPTIONS": {
                    "sslmode": "require",
                },
            },
        },
        SECRET_KEY="test",
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "rest_framework",
            "supa_auth",
        ),
        AUTH_USER_MODEL="supa_auth.SupaUser",
        PASSWORD_HASHERS=[
            "supa_auth.hashers.SupabasePasswordHasher",
        ],
        SIMPLE_JWT={
            "JTI_CLAIM": None,
            "TOKEN_TYPE_CLAIM": None,
            "USER_ID_CLAIM": "sub",
            "SIGNING_KEY": "test",
            "VERIFYING_KEY": "test",
        },
        TIME_ZONE="UTC",
        USE_I18N=True,
        USE_TZ=True,
    )

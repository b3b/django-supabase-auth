import pytest
from django.conf import settings
from environs import Env

from .fixtures import *  # noqa

env = Env()
env.read_env()


def pytest_configure():
    settings.configure(
        SUPABASE_URL=env("SUPABASE_URL"),
        SUPABASE_API_KEY=env("SUPABASE_API_KEY"),
        DATABASES={
            "default": {
                "ENGINE": "supa_auth",
                "HOST": env("SUPABASE_HOST"),
                "USER": env("SUPABASE_USER"),
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
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            },
        ],
        TIME_ZONE="UTC",
        USE_I18N=True,
        USE_TZ=True,
    )


def pytest_addoption(parser):
    parser.addoption(
        "--live-db",
        action="store_true",
        default=False,
        help="Run tests that use the live ('postgres') database",
    )


def pytest_runtest_setup(item):
    if item.config.getoption("--live-db"):
        if "livedb" in item.keywords:
            settings.DATABASES["default"]["TEST"]["NAME"] = "postgres"
        else:
            pytest.skip("test should not run on live database")
    elif "livedb" in item.keywords:
        pytest.skip("test should run on live database")

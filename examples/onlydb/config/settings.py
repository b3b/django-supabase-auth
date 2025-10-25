"""
Django settings for `onlydb` project example.
"""
from .base_settings import *  # noqa
from .base_settings import env

SUPABASE_HOST = env("SUPABASE_HOST")
SUPABASE_USER = env("SUPABASE_USER")
SUPABASE_PASSWORD = env("SUPABASE_PASSWORD")

DATABASES = {
    "default": {
        "ENGINE": "supa_auth",
        "HOST": SUPABASE_HOST,
        "USER": SUPABASE_USER,
        "PASSWORD": SUPABASE_PASSWORD,
        "SCHEMA": "onlydb",
        "OPTIONS": {
            "sslmode": "require",
        },
    },
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "supa_auth.apps.NoModels",
    "onlydb",
]

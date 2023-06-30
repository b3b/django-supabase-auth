"""
Django settings for `localdb` project example.
"""
from .base_settings import *  # noqa
from .base_settings import env

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "testapp",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication",
    ],
}

SIMPLE_JWT = {
    "TOKEN_USER_CLASS": "supa_auth.models.SupaTokenUser",
    "JTI_CLAIM": None,
    "TOKEN_TYPE_CLAIM": None,
    "USER_ID_CLAIM": "sub",
    "SIGNING_KEY": env("SUPABASE_JWT_SECRET"),
    "VERIFYING_KEY": env("SUPABASE_JWT_SECRET"),
}

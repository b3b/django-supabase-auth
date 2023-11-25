"""
Django settings for `remotedb` project example.
"""
from .base_settings import *  # noqa
from .base_settings import env

DATABASES = {
    "default": {
        "ENGINE": "supa_auth",
        "HOST": env("SUPABASE_HOST"),
        "PASSWORD": env("SUPABASE_PASSWORD"),
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
    "rest_framework",
    "supa_auth",
    "testapp",
]

AUTH_USER_MODEL = "supa_auth.SupaUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}

SIMPLE_JWT = {
    "TOKEN_USER_CLASS": "supa_auth.models.SupaUser",
    "JTI_CLAIM": None,
    "TOKEN_TYPE_CLAIM": None,
    "USER_ID_CLAIM": "sub",
    "SIGNING_KEY": env("SUPABASE_JWT_SECRET"),
    "VERIFYING_KEY": env("SUPABASE_JWT_SECRET"),
}

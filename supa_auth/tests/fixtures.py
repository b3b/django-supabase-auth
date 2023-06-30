import jwt
import pytest
from django.conf import settings


@pytest.fixture
def token_payload():
    return {
        "aud": "authenticated",
        "exp": 9999999999,
        "sub": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        "email": "user@xample.org",
        "phone": "",
        "app_metadata": {"provider": "email", "providers": ["email"]},
        "user_metadata": {},
        "role": "authenticated",
    }


@pytest.fixture
def superuser_token_payload():
    return {
        "aud": "authenticated",
        "exp": 9999999999,
        "sub": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "email": "user@xample.org",
        "phone": "",
        "app_metadata": {
            "is_staff": True,
            "is_superuser": True,
            "provider": "email",
            "providers": ["email"],
        },
        "user_metadata": {},
        "role": "authenticated",
    }


@pytest.fixture
def anonymous_token_payload():
    return {
        "iss": "supabase",
        "ref": "projectcodename",
        "role": "anon",
        "iat": 1686302075,
        "exp": 9999999999,
    }


@pytest.fixture
def access_token(token_payload):
    return generate_token(token_payload)


@pytest.fixture
def expired_access_token(token_payload):
    token_payload["exp"] = 1686302075
    return generate_token(token_payload)


@pytest.fixture
def anonymous_access_token(anonymous_token_payload):
    return generate_token(anonymous_token_payload)


def generate_token(payload):
    return jwt.encode(payload, settings.SIMPLE_JWT["SIGNING_KEY"], algorithm="HS256")

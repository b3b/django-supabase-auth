import jwt
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection


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


@pytest.fixture
def valid_password_hash():
    return "$2a$10$p8.1/EFwSnX2PEuBkjKkZePYiRqGClm3h9fVaivzV1f26pFDowYYO"


@pytest.fixture
def valid_password():
    return "1234"


@pytest.fixture
def valid_password_salt():
    return b"$2a$10$p8.1/EFwSnX2PEuBkjKkZe"


@pytest.fixture
def invalid_password():
    return "12345"


@pytest.fixture
def valid_user_from_sql(db, valid_password_hash):
    uid = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0"
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO auth.users (id, email, encrypted_password,
                                    email_confirmed_at, raw_app_meta_data)
            VALUES (%s, %s, %s, %s, %s::json);
            """,
            [
                uid,
                "user@example.com",
                valid_password_hash,
                "2023-01-01 00:00:00",
                '{"provider": "email", "providers": ["email"]}',
            ],
        )
        return get_user_model().objects.get(id=uid)


# @pytes
@pytest.fixture
def valid_superuser_from_sql(db, valid_password_hash):
    uid = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1"
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO auth.users (id, email, encrypted_password,
                                    email_confirmed_at, raw_app_meta_data)
            VALUES (%s, %s, %s, %s, %s::json);
            """,
            [
                uid,
                "admin@example.com",
                valid_password_hash,
                "2023-01-01 00:00:00",
                (
                    '{"provider": "email", "providers": ["email"],'
                    ' "is_staff": true, "is_superuser": true}'
                ),
            ],
        )
    return get_user_model().objects.get(id=uid)

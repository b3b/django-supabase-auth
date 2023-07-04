# pylint: disable=no-member
from django.contrib.auth import models as auth_models

from supa_auth.models import SupaTokenUser, SupaUser


def test_token_user_is_valid(token_payload):
    user = SupaTokenUser(token_payload)
    assert user.id == "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    assert not user.username
    assert not user.is_staff
    assert not user.is_superuser


def test_token_superuser_is_valid(superuser_token_payload):
    user = SupaTokenUser(superuser_token_payload)
    assert user.id == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    assert not user.username
    assert user.is_staff
    assert user.is_superuser


def test_user_model_is_swapped():
    """Test that Django User model has been swapped out."""
    assert auth_models.User._meta.swapped


def test_user_default_fields(db):
    user = SupaUser.objects.create()
    assert user.id
    assert not user.email
    assert not user.phone
    assert not user.password
    assert not user.last_login

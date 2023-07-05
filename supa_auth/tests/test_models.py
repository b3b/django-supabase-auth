# pylint: disable=no-member
from django.contrib.auth import models as auth_models
from django.utils import timezone

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

    assert not user.is_staff
    assert not user.is_superuser


def test_user_created_from_sql(db, valid_user_from_sql):
    obj = valid_user_from_sql
    assert obj.id
    assert obj.is_active
    assert not obj.is_staff
    assert not obj.is_superuser


def test_superuser_created_from_sql(db, valid_superuser_from_sql):
    obj = valid_superuser_from_sql
    assert obj.id
    assert obj.is_active
    assert obj.is_staff
    assert obj.is_superuser


def test_is_staff_attribute_saved(db):
    assert SupaUser.objects.filter(is_staff=True).count() == 0
    assert SupaUser.objects.filter(is_staff=False).count() == 0

    user = SupaUser.objects.create()
    assert not user.is_staff
    assert SupaUser.objects.filter(is_staff=True).count() == 0
    assert SupaUser.objects.filter(is_staff=False).count() == 1

    user.is_staff = True
    assert user.is_staff
    assert SupaUser.objects.filter(is_staff=True).count() == 0
    assert SupaUser.objects.filter(is_staff=False).count() == 1

    user.save()
    user.refresh_from_db()

    assert user.is_staff
    assert SupaUser.objects.filter(is_staff=True).count() == 1
    assert SupaUser.objects.filter(is_staff=False).count() == 0


def test_is_superuser_attribute_saved(db):
    assert SupaUser.objects.filter(is_superuser=True).count() == 0
    assert SupaUser.objects.filter(is_superuser=False).count() == 0

    user = SupaUser.objects.create()
    assert not user.is_superuser
    assert SupaUser.objects.filter(is_superuser=True).count() == 0
    assert SupaUser.objects.filter(is_superuser=False).count() == 1

    user.is_superuser = True
    assert user.is_superuser
    assert SupaUser.objects.filter(is_superuser=True).count() == 0
    assert SupaUser.objects.filter(is_superuser=False).count() == 1

    user.save()
    user.refresh_from_db()

    assert user.is_superuser
    assert SupaUser.objects.filter(is_superuser=True).count() == 1
    assert SupaUser.objects.filter(is_superuser=False).count() == 0


def test_user_is_active_saved(db):
    assert SupaUser.objects.filter(is_active=True).count() == 0
    assert SupaUser.objects.filter(is_active=False).count() == 0

    user = SupaUser.objects.create(email_confirmed_at=timezone.now())
    assert user.is_active
    assert SupaUser.objects.filter(is_active=True).count() == 1
    assert SupaUser.objects.filter(is_active=False).count() == 0

    user.is_active = False
    assert not user.is_active
    assert SupaUser.objects.filter(is_active=True).count() == 1
    assert SupaUser.objects.filter(is_active=False).count() == 0

    user.save()
    assert SupaUser.objects.filter(is_active=True).count() == 0
    assert SupaUser.objects.filter(is_active=False).count() == 1

    user = SupaUser.objects.get()
    assert not user.is_active

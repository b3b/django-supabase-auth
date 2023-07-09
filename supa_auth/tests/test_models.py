# pylint: disable=no-member
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
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

    assert str(user.instance_id) == "00000000-0000-0000-0000-000000000000"
    assert user.app_metadata == {"provider": "email", "providers": ["email"]}
    assert user.aud == "authenticated"
    assert user.role == "authenticated"
    assert user.created_at
    assert user.updated_at


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


def test_user_group_added(db):
    user = SupaUser.objects.create()
    group = auth_models.Group.objects.create(name="test-1")

    user.groups.add(group)

    assert SupaUser.objects.filter(groups__name="test-1").get() == user


def test_permission_added(db):
    user = SupaUser.objects.create(email_confirmed_at=timezone.now())
    permission = Permission.objects.create(
        codename="test_permission",
        name="Test Permission",
        content_type=ContentType.objects.get_for_model(SupaUser),
    )

    user.user_permissions.add(permission)

    assert user.has_perm("supa_auth.test_permission")
    assert user.user_permissions.filter(codename="test_permission").exists()


def test_valid_user_created_with_create_user(db):
    user = SupaUser.objects.create_user()
    assert user.pk
    assert user.password
    assert not user.check_password("")
    assert not user.email
    assert not user.is_staff
    assert not user.is_superuser


def test_user_created_with_custom_metadata(db):
    user = SupaUser.objects.create_user(app_metadata={"providers": ["github"]})
    assert user.app_metadata == {"providers": ["github"]}


def test_valid_user_created_with_create_superuser(db):
    user = SupaUser.objects.create_superuser()
    assert user.pk
    assert user.password
    assert not user.check_password("")
    assert not user.email
    assert not user.is_staff
    assert not user.is_superuser


def test_check_password_valid_password(
    db, valid_superuser_from_sql, valid_password, valid_password_hash
):
    assert valid_superuser_from_sql.password == valid_password_hash
    assert valid_superuser_from_sql.check_password(valid_password)
    assert valid_superuser_from_sql.password == valid_password_hash


def test_password_changed(db):
    user = SupaUser.objects.create_user(password="original")
    assert user.check_password("original")
    user.set_password("changed")
    assert not user.check_password("original")
    assert user.check_password("changed")


def test_check_password_invalid_password(
    db, valid_superuser_from_sql, invalid_password
):
    assert not valid_superuser_from_sql.check_password(invalid_password)

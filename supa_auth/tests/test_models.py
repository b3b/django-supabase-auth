from supa_auth.models import SupaTokenUser


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

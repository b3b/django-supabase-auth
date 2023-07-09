from django.contrib.auth.hashers import BCryptPasswordHasher

from supa_auth.hashers import EmptyStringAlgorithm, SupabasePasswordHasher


def test_algotithm_class():
    algo = EmptyStringAlgorithm()
    assert algo
    assert algo == ""
    assert {algo: "expected"}[""] == "expected"
    assert {"": "expected"}[algo] == "expected"
    assert len(algo) == 0
    assert f"123{algo}4" == "1234"


def test_password_encoded(valid_password, valid_password_hash, valid_password_salt):
    encoded = SupabasePasswordHasher().encode(
        "1234",
        valid_password_salt,
    )
    assert encoded == valid_password_hash


def test_encrypted_password_differs_from_bcrypt_hasher_only_by_prefix():
    password = "test-password"
    salt = b"$2b$10$D2opeDQIMW9jS1iIjNQs8e"
    assert BCryptPasswordHasher().encode(
        password, salt
    ) == "bcrypt$" + SupabasePasswordHasher().encode(password, salt)

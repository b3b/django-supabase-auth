"""supa_auth.hashers"""
from django.contrib.auth.hashers import BCryptPasswordHasher


class EmptyStringAlgorithm:
    """String-like class representing an "" password algorithm."""

    def __bool__(self) -> bool:
        """Return True to indicate that the algorithm is set."""
        return True

    def __eq__(self, other) -> bool:
        """Compare the instance.

        Instance is equal to and empty string.
        """
        return str(other) == ""

    def __hash__(self):
        """Compute the hash value.

        Instance can be used as a key in a dictionary,
        that is equal to an empty string.
        """
        return hash("")

    def __len__(self) -> int:
        """Return the length of the algorithm string."""
        return 0

    def __str__(self) -> str:
        """Return the string representation of the algorithm (an empty string)."""
        return ""


class SupabasePasswordHasher(BCryptPasswordHasher):
    """Password hasher for Supabase user model'.

    This hasher extends the BCryptPasswordHasher to encode passwords
    in the Supabase 'auth.users' format: $<iterations>$<salt>$<hash> ,
    instead if the original Django format: <algorithm>$$<iterations>$<salt>$<hash> .
    """

    # `EmptyStringAlgorithm` is used instead of just "" so that
    # the algorithm can be found found in the Django PASSWORD_HASHERS setting.
    algorithm = EmptyStringAlgorithm()

    # The same number of bcrypt encoding rounds is used
    # as currently set by Supabase.
    rounds = 10

    def must_update(self, encoded) -> bool:
        """Determine if the encoded password must be updated.

        In this hasher, the encoded password is never considered outdated,
        so Django will not try to update the password.
        """
        return False

    def encode(self, password: str, salt: bytes) -> str:
        """Encode the password."""
        encoded = super().encode(password=password, salt=salt)
        if not encoded.startswith("$$"):
            raise ValueError("Unexpected password encoding format.")
        # remove the extra "$" starting character
        return encoded[1:]

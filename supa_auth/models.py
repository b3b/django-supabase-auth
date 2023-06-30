"""'supa_auth' app models."""
# pylint: disable=abstract-method,invalid-overridden-method
from rest_framework_simplejwt.models import TokenUser


class SupaTokenUser(TokenUser):
    """A class that implements the `auth.User` interface.

    Instances of this class act as stateless user objects,
    which has no database presentation and are backed by validated tokens.
    Extends the functionality of Simple JWT `TokenUser`
    to support Supabase-specific user metadata.
    """

    @property
    def app_metadata(self) -> dict:
        """Application metadata."""
        return self.token["app_metadata"]

    @property
    def is_active(self) -> bool:
        """
        Property indicating if the user is active.
        It is always True since the token was issued by Supabase.
        """
        return True

    @property
    def is_staff(self) -> bool:
        """
        Property indicating whether this user can access the admin site.
        Retrieves the value of 'is_staff'
        from the 'app_metadata' field in the token.
        """
        return self.app_metadata.get("is_staff", False)

    @property
    def is_superuser(self) -> bool:
        """
        Property indicating that this user has all permissions
        without explicitly assigning them.
        Retrieves the value of 'is_superuser'
        from the 'app_metadata' field in the token.
        """
        return self.app_metadata.get("is_superuser", False)

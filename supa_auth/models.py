"""'supa_auth' app models."""
# pylint: disable=abstract-method,invalid-overridden-method,missing-docstring
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
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


class SupabaseUserManager(UserManager):
    """Manager for SupaUser model."""


class SupaUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model for Supabase.

    It serves as a wrapper for the original Supabase `auth.users` table.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True, default=None)

    password = models.CharField(
        _("password"), max_length=255, db_column="encrypted_password"
    )
    last_login = models.DateTimeField(
        _("last login"), blank=True, null=True, db_column="last_sign_in_at"
    )
    is_superuser = True
    is_staff = True

    objects = SupabaseUserManager()

    USERNAME_FIELD = "id"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        app_label = "supa_auth"
        db_table = '"auth"."users"'
        managed = False

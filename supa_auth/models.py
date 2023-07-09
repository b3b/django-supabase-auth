"""'supa_auth' app models."""
# pylint: disable=abstract-method,arguments-renamed,invalid-overridden-method
# pylint: disable=missing-docstring
import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    Group,
    Permission,
    PermissionsMixin,
    UserManager,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.models import TokenUser

from . import settings as app_settings
from .fields import BooleanAppMetadataField, IsActiveField


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


class UserGroup(models.Model):
    user = models.ForeignKey("supa_auth.SupaUser", on_delete=models.CASCADE)
    group = models.ForeignKey("auth.Group", on_delete=models.CASCADE)

    class Meta:
        app_label = "supa_auth"
        db_table = "auth_user_groups"


class UserPermission(models.Model):
    user = models.ForeignKey("supa_auth.SupaUser", on_delete=models.CASCADE)
    permission = models.ForeignKey("auth.Permission", on_delete=models.CASCADE)

    class Meta:
        app_label = "supa_auth"
        db_table = "auth_user_permissions"


class SupabaseUserManager(UserManager):
    """Manager for SupaUser model."""

    def get_queryset(self):
        """Get the queryset for the SupaUser model
        with field annotations defined using `FieldWithAnnotation` fields.
        """
        qs = super().get_queryset()
        return qs.annotate(**self.model._field_annotations)

    def _create_user(self, email=None, phone=None, password=None, **extra_fields):
        """A helper method to create and save a user with optional email and phone."""
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.password = make_password(password)
        return user

    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        """Create a regular user"""
        user = self._create_user(
            email=email, phone=phone, password=password, **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        """Create a superuser."""
        user = self._create_user(
            email=email, phone=phone, password=password, **extra_fields
        )
        user.save(using=self._db)
        return user


class SupaUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model for Supabase.

    It serves as a wrapper for the original Supabase `auth.users` table.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instance_id = models.UUIDField(
        _("unused"), null=True, editable=False, default=app_settings.DEFAULT_INSTANCE_ID
    )
    aud = models.CharField(
        max_length=255, blank=True, null=True, default=app_settings.DEFAULT_AUDIENCE
    )
    role = models.CharField(
        max_length=255, blank=True, null=True, default=app_settings.DEFAULT_ROLE
    )
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True, default=None)
    is_sso_user = models.BooleanField(default=False)

    password = models.CharField(
        _("password"), max_length=255, db_column="encrypted_password"
    )
    last_login = models.DateTimeField(
        _("last login"), blank=True, null=True, db_column="last_sign_in_at"
    )

    banned_until = models.DateTimeField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    email_confirmed_at = models.DateTimeField(blank=True, null=True, default=None)
    phone_confirmed_at = models.DateTimeField(blank=True, null=True, default=None)

    user_metadata = models.JSONField(
        _("user metadata"),
        blank=True,
        null=True,
        db_column="raw_user_meta_data",
        help_text=_("User-specific info. Can be modified by regular user."),
    )
    app_metadata = models.JSONField(
        _("application metadata."),
        blank=True,
        null=True,
        db_column="raw_app_meta_data",
        default=lambda: dict(app_settings.DEFAULT_APP_METADATA),
        help_text=_("Application specific metadata. Only a service role can modify."),
    )

    is_active = IsActiveField()
    is_superuser = BooleanAppMetadataField()
    is_staff = BooleanAppMetadataField()

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
        through="supa_auth.UserGroup",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
        through="supa_auth.UserPermission",
    )

    objects = SupabaseUserManager()

    USERNAME_FIELD = "id"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        app_label = "supa_auth"
        db_table = '"auth"."users"'
        managed = False

    def __str__(self):
        return f"{self.email or self.phone or self.id}"

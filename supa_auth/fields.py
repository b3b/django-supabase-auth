"""supa_auth.fields"""
from abc import ABC, abstractmethod
from typing import Any

from django.db.models import BooleanField, Case, Model, Q, Value, When
from django.utils import timezone

from . import settings as app_settings


class FieldWithAnnotation(ABC):
    """Base class for custom fields with annotation functionality.

    It allows custom fields to contribute annotations to the model class,
    which can be used in queries.
    The field annotation will be stored in the `_field_annotations` attribute of model.

    :param field_name:
        The name of the field.
        If not provided, it will be inferred from the attribute name.
    :param annotation: The annotation to be added to the model field.
    :param default: The default value for the field.
    """

    def __init__(self, *, field_name=None, annotation=None, default=None):
        self.field_name = field_name
        self.annotation = annotation
        self.default = default

    @abstractmethod
    def __get__(
        self, instance: Model | None, owner: Any
    ) -> "FieldWithAnnotation | Any":
        """Retrieve the value of the field from the instance."""
        if instance is None:
            return self
        return ...

    @abstractmethod
    def __set__(self, instance: Model, value: Any):
        """Set the value of the field on the instance."""

    def contribute_to_class(self, cls, name, **kwargs):
        """Register the field annotation with the model class."""
        if not self.field_name:
            self.field_name = name
        setattr(cls, name, self)
        if self.annotation:
            annotations = getattr(cls, "_field_annotations", {})
            annotations[self.field_name] = self.annotation
            cls._field_annotations = annotations


class AppMetadataField(FieldWithAnnotation):
    """Field that represents a value from the metadata JSON field.

    This field allows accessing and setting values
    from the `app_metadata` JSON field of the Supabase user.

    When accessed, it retrieves the corresponding value from the metadata JSON field.
    If the value is not found, it returns the default value specified for the field.
    When set, it updates the metadata JSON field with the new value.
    """

    def __get__(self, instance, owner):
        """Retreive the value from the metadata JSON field."""
        if instance is None:
            return self
        return (instance.app_metadata or {}).get(self.field_name, self.default)

    def __set__(self, instance, value):
        """Set the value un the metadata JSON field."""
        metadata = instance.app_metadata or {}
        metadata.pop(self.field_name, None)
        if value:
            metadata[self.field_name] = value


class BooleanAppMetadataField(AppMetadataField):
    """A custom field for representing boolean values in the 'app_metadata' JSON field.

    It simplifies the annotation expression to
    return True only when `app_metadata__field_name=True`
    and `False` otherwise.
    """

    def contribute_to_class(self, cls, name, **kwargs):
        if not self.field_name:
            self.field_name = name
        self.annotation = Case(
            When(**{f"app_metadata__{self.field_name}": True}, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
        super().contribute_to_class(cls, name, **kwargs)


class IsActiveField(FieldWithAnnotation):
    """Field that indicates the active status of the Supabase user.

    This field represents the active status of the user based on certain conditions
    such as email confirmation, phone confirmation, and ban status.

    When set to `True`, it sets the `banned_until` field to `None`
    indicating an active user.
    When set to `False`, it sets the `banned_until` field to a high future value.
    """

    def __init__(self):
        super().__init__(
            annotation=Q(
                (
                    Q(email_confirmed_at__isnull=False)
                    | Q(phone_confirmed_at__isnull=False)
                )
                & (Q(banned_until__isnull=True) | Q(banned_until__lt=timezone.now()))
            )
        )

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return bool(
            (instance.email_confirmed_at or instance.phone_confirmed_at)
            and (
                instance.banned_until is None or instance.banned_until < timezone.now()
            )
        )

    def __set__(self, instance: Model, value: bool):
        instance.banned_until = None if value else app_settings.BAN_FOREVER_TIME

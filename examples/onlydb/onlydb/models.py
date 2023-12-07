"""'onlydb' models."""
# pylint: disable=missing-class-docstring,no-member
from django.db import models


class Private(models.Model):
    """Model that is private to the Django app."""

    def __str__(self):
        return str(self.id)


class Public(models.Model):
    """Model that is exposed to the Supabase data API
    due to its table storage in the "public" schema.
    """

    class Meta:
        db_table = '"public"."onlydb_published"'

    def __str__(self):
        return str(self.id)

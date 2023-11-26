"""'testapp' models."""
from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    """Profile model for a Supabase user.

    Represents additional information associated with a user.
    """

    user = models.OneToOneField(
        get_user_model(), primary_key=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    preferred_username = models.CharField(
        max_length=255, blank=True, null=True, default=None
    )

    def __str__(self):
        return str(self.preferred_username or self.user)

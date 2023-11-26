# pylint: disable=missing-class-docstring
from django.contrib import admin
from testapp.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    raw_id_fields = ("user",)
    readonly_fields = ("created_at", "updated_at")

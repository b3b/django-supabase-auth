"""'onlydb' admin site."""
# pylint: disable=missing-class-docstring,no-member
from django.contrib import admin
from onlydb import models


@admin.register(models.Private)
class PrivateAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Public)
class PublicAdmin(admin.ModelAdmin):
    pass

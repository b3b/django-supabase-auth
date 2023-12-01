"""'supa_auth' admin site."""
# pylint: disable=missing-class-docstring,no-member
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from supa_auth.models import SupaUser


class BooleanFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        return [(True, _("True")), (False, _("False"))]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(is_active=self.value())
        return None


class IsActiveFilter(BooleanFilter):
    title = _("Is active")
    parameter_name = "is_active"


class IsSuperUser(BooleanFilter):
    title = _("Is Superuser")
    parameter_name = "is_superuser"


class GroupInlineAdmin(admin.TabularInline):
    model = SupaUser.groups.through
    extra = 0


class PermissionInlineAdmin(admin.TabularInline):
    model = SupaUser.user_permissions.through
    extra = 0


@admin.register(SupaUser.groups.through)
class SupaUserGroupAdmin(admin.ModelAdmin):
    list_display = ("user", "group")
    raw_id_fields = ("user",)


@admin.register(SupaUser.user_permissions.through)
class SupaUserPermissionAdmin(admin.ModelAdmin):
    list_display = ("user", "permission")
    raw_id_fields = ("user",)


@admin.register(SupaUser)
class SupaUserAdmin(UserAdmin):
    readonly_fields = (
        "is_active",
        "is_superuser",
        "is_staff",
        "created_at",
        "updated_at",
        "last_login",
    )
    inlines = (GroupInlineAdmin, PermissionInlineAdmin)

    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("is_sso_user", "email", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "last_login",
                    "banned_until",
                    "email_confirmed_at",
                    "phone_confirmed_at",
                )
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("user_metadata", "app_metadata"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("password1", "password2"),
            },
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("id", "email", "phone", "is_active")
    list_filter = (
        "groups",
        IsActiveFilter,
        IsSuperUser,
    )
    search_fields = ("email", "phone")
    ordering = ("-created_at",)

    @admin.display(boolean=True)
    def is_active(self, obj):
        return obj.is_active


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("content_type")

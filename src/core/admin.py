from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdminUser

from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import CustomeUser
# Register your models here.


class CustomeUserAdmin(BaseAdminUser):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email",  "is_admin", "national_code"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "national_code", "is_active", "last_login"]}),
        ("Personal info", {"fields": ["date_of_birth"]}),
        ("Permissions", {"fields": ["is_admin", "is_superuser"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "date_of_birth", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email","national_code"]
    ordering = ["is_admin", "email","national_code" ]
    filter_horizontal = []

admin.site.register(CustomeUser ,CustomeUserAdmin)
admin.site.unregister(Group)
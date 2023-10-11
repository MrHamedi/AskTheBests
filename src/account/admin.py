from django.contrib import admin
from core.models import Profile
from django.contrib.auth.models import User




class ProfileAdmin(admin.ModelAdmin):
    list_display=("user","pic","code")
    search_fields=("user__email","code")
    date_hierarchy="user__date_joined"


admin.site.register(Profile,ProfileAdmin)
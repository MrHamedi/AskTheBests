from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User




class ProfileAdmin(admin.ModelAdmin):
    list_display=("user","name","pic","code")
    search_fields=("user__username","code","user__first_name","user__last_name")
    date_hierarchy="user__date_joined"

    """
        This function will return the full name of user 
    """
    def name(self,obj):
        return(obj.user.first_name+" "+obj.user.last_name)


admin.site.register(Profile,ProfileAdmin)
from django.contrib import admin
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields=("publish","upd_date")
    list_display=("author","score")
    list_filter=("author","score")
    fieldsets=(
            (None,{"fields":("author","slug","publish")}),
            ("Info",{"classes":("collapse",),"fields":("score","title","body")})
    )


# Register your models here.
admin.site.register(Question,QuestionAdmin)
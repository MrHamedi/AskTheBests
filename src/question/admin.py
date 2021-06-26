from django.contrib import admin
from .models import Comment, Question,Comment


class QuestionAdmin(admin.ModelAdmin):
    """
        This is the admin class for Question model 
    """

    readonly_fields=("publish","update")
    list_display=("author","score","publish")
    list_filter=("author","score")
    fieldsets=(
            (None,{"fields":("author","slug","publish","update","tags")}),
            ("Info",{"classes":("collapse",),"fields":("score","title","body","liked_by","disliked_by")})
    )


class CommentAdmin(admin.ModelAdmin):
    """
        This is the admin class for Comment model 
    """
    readonly_fields=("update","publish")
    list_display=("question","author","publish","update")
    list_filter=("question","author","publish")
    search_fields=("content","pk")
    fieldsets=(
        (None,{"fields":("question","publish","update")}),
        ("Info",{"fields":("score","content","liked_by","disliked_by"),"classes":"collapse"})
    )

    class Meta:
        ordering=("publish",)



# Register your models here.
admin.site.register(Question,QuestionAdmin)
admin.site.register(Comment,CommentAdmin)

from django.db import models
from django.contrib import auth 


class Question(models.Model):
    """
        This is the Question model 
    """
    title=models.CharField(help_text="The title of question",verbose_name="Title of question",max_length=200)
    body=models.TextField(verbose_name="The question")
    publish=models.DateTimeField(auto_now_add=True,help_text="The publish date of post")
    upd_date=models.DateTimeField()
    author=models.ForeignKey(auth.get_user_model(),on_delete=models.CASCADE,related_name="questions")
    score=models.DecimalField(max_digits=3,default=0,decimal_places=1)
    slug=models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering=("-publish",)
        unique_together=("author","publish")

    def __str__(self):
        return(self.title)

    
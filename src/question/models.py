from django.db import models
from django.contrib import auth 
from taggit.managers import TaggableManager
from django.urls import reverse
from django.contrib.auth.models import User 
from account.models import Profile 

class Question(models.Model):
    """
        This is the Question model 
    """
    title=models.CharField(help_text="The title of question",verbose_name="Title of question",max_length=200)
    body=models.TextField(verbose_name="The question")
    publish=models.DateTimeField(auto_now_add=True,help_text="The publish date of post")
    update=models.DateTimeField(verbose_name="The last update",auto_now=True)
    author=models.ForeignKey(auth.get_user_model(),on_delete=models.CASCADE,related_name="questions")
    score=models.IntegerField(help_text="The score of this question",default=0)
    slug=models.SlugField(max_length=200,unique=True)
    tags=TaggableManager()
    liked_by=models.ManyToManyField(Profile,related_name="liked_by",blank=True)
    disliked_by=models.ManyToManyField(Profile,related_name="disliked_by",blank=True)


    class Meta:
        ordering=("-publish",)
        unique_together=("author","publish")

    def get_absolute_url(self):
        return(reverse("question:questionDetail",args=[self.pk]))

    def __str__(self):
        return(self.title)

    def slug_maker(self):
        """
            This function will create object slug in CreateView
        """
        slug=self.title+self.author.username+str(self.id)
        return(slug)

class Comment(models.Model):
    """
        This model is for client comments on question
    """
    author=models.ForeignKey(auth.get_user_model(),on_delete=models.SET_DEFAULT ,default=1,help_text="The author of comment")
    question=models.ForeignKey(Question,on_delete=models.PROTECT,help_text="The question that this comment has been written for",null=True,related_name="comments")
    content=models.TextField(verbose_name="Comment")
    score=models.IntegerField(help_text="The score of this comment")    
    publish=models.DateTimeField(help_text="The publish time of this comment",verbose_name="Publish time",auto_now_add=True)
    update=models.DateTimeField(help_text="The time of the last editting of this comment",verbose_name="Last update time",auto_now=True)

    class Meta:
        ordering=("-publish",)

    def __str__(self):
        return(self.content)





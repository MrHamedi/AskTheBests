from taggit.managers import TaggableManager

from django.db import models
from django.contrib import auth 
from django.urls import reverse
from django.utils.text import slugify

from core.models import TimeStampMixin, Profile


class Question(TimeStampMixin):
    """
        This is the Question model 
    """
    title=models.CharField(help_text="The title of question",verbose_name="Title of question",max_length=200)
    body=models.TextField(verbose_name="The question")
    author=models.ForeignKey(auth.get_user_model(),on_delete=models.CASCADE,related_name="questions")
    score=models.IntegerField(help_text="The score of this question",default=0)
    slug=models.SlugField(max_length=200,unique=True)
    tags=TaggableManager()
    liked_by=models.ManyToManyField(Profile,related_name="liked_by",blank=True)
    disliked_by=models.ManyToManyField(Profile,related_name="disliked_by",blank=True)


    class Meta:
        ordering=("-publish",)
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_titles_for_each_author",
            )
        ]

    def get_absolute_url(self):
        return(reverse("question:questionDetail",args=[self.pk]))

    def __str__(self):
        return(self.title)
    
    def save(self, *args, **kwargs):
        if(not self.slug):
            base_slug=slugify(self.title)
            if(Question.objects.filter(slug=base_slug).exists()):
                base_slug=base_slug+f"{self.author.id}"
                self.slug=base_slug
                super().save(*args, **kwargs)
            else:
                self.slug=base_slug
            super().save(*args, **kwargs)


class Comment(TimeStampMixin):
    """
        This model is for client comments on question
    """
    author=models.ForeignKey(auth.get_user_model(),on_delete=models.SET_DEFAULT ,default=1,help_text="The author of comment")
    question=models.ForeignKey(Question,on_delete=models.PROTECT,help_text="The question that this comment has been written for",null=True,related_name="comments")
    content=models.TextField(verbose_name="Comment")
    score=models.IntegerField(help_text="The score of this comment")    
    liked_by=models.ManyToManyField(Profile,related_name="comment_liked_by",blank=True)
    disliked_by=models.ManyToManyField(Profile,related_name="comment_disliked_by",blank=True)


    class Meta:
        ordering=("-publish",)

    def __str__(self):
        return(self.content)

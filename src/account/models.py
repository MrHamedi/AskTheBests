from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    pic=models.ImageField(upload_to="profile_image/%Y/%m/%d/",verbose_name="picture")
    code=models.CharField(max_length=6)    
    code_limit_time=models.DateTimeField(help_text="The expiration date of this activsion code")
    score=models.IntegerField(help_text="The score of this person")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    
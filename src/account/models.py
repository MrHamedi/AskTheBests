from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    pic = models.ImageField(upload_to="profile_image/%Y/%m/%d/",
                            verbose_name="picture", null=True, blank=True)
    code = models.CharField(max_length=6, null=True)
    code_limit_time = models.DateTimeField(
        help_text="The expiration date of this activsion code", null=True, blank=True)
    score = models.IntegerField(
        help_text="The score of this person", default=0)
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile")

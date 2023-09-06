from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# Create your models here.


class CustomeUserManager(BaseUserManager):

    def create_user(self, email,  password=None, **extra_fields):  
        if(not email):
            raise ValueError("فیلد ایمیل ضرورری است!")
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, national_code, date_of_birth, password=None, **extra_fields):
        if (not national_code):
            raise ValueError(" کد ملی برای ادمین ضروری است!")
        
        if (not date_of_birth):
            raise ValueError("تاریخ تولد ادمین باید مشخص باشد!")

        user = self.create_user(email, date_of_birth=date_of_birth, national_code=national_code, password=password)
        user.is_admin=True 
        user.save(using=self._db)
        return user

class CustomeUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=225,
        unique=True,
        verbose_name='آدرس ایمیل'
    )
    date_joined = models.DateTimeField(
                                        verbose_name='تاریخ ثبت عضویت',
                                       auto_now_add=True,
                                       editable=False)
    national_code = models.IntegerField(verbose_name='کد ملی', unique=True, blank=True, null=True)
    date_of_birth=models.DateField(
        verbose_name='تاریخ تولد',
        null=True,
        blank=True,
    )
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    
    objects=CustomeUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    ReQUIRED_FIELDS = ['date_of_birth', 'national_code']
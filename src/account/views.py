import json
import datetime
import random 
from rest_framework import generics, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated


from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.mail import send_mail

from .forms  import account_activator, login_form,register_form
from .models import Profile
from .utils import database_checker
from .serializers import (UserCreationSerializer, TokenSerializer, 
                         UserInfoUpdateSerializer)


def login_view(request):
    next_page=request.POST.get("next")
    if(request.method=="POST"):
        form=login_form(data=request.POST)
        if(form.is_valid()):
            cd=form.cleaned_data 
            user=authenticate(username=cd["username"],password=cd["password"])
            if(user):
                if(user.is_active):
                    login(request,user)
                    if(next_page):
                        return(HttpResponseRedirect(next_page))
                    else:
                        return(redirect("question:homepage"))

            else:
                messages.error(request,mark_safe("User does not exist ! <br> please check your password and username."))
    else:
        form=login_form()
    return(render(request,"account/login.html",{"form":form}))


def logout_view(request):
    user=request.user 
    logout(request)
    return(render(request,"account/logout.html"))


def register_view(request):
    if(request.method=="POST"):
        form=register_form(data=request.POST)
        if(form.is_valid()):
            cd=form.cleaned_data
            #check if there is any user in database with this username or email
            if(database_checker("auth","User",username=cd["username"])):
                messages.error(request,"This username have been taken! please choose another one.")
            elif(database_checker("auth","User",email=cd["email"])):
                messages.error(request,"This email adress have been taken! please choose another one.")
            else:
                user=User(username=cd["username"],email=cd["email"])
                user.set_password(cd["password"])
                user.is_active=False
                user.save()
                profile=Profile(user=user)
                profile.save()
                return(redirect("account:account_activator_view",user.username))
    else:
        form=register_form()
    return(render(request,"account/register_page.html",{"form":form}))

"""
    This function will create random number and send it to client email
"""

def code_sender_view(request,username):
    user=User.objects.get(username=username)
    code=""
    #We create the activision code 
    for i in range(0,6):
        number=random.randrange(0,9)
        code+=str(number)    
    profile=user.profile
    profile.code_limit_time=datetime.datetime.now()+datetime.timedelta(minutes=5)
    profile.code=code
    profile.save()
    #We send code to client email 
    subject="Account activision code from AB site."
    message=f"Hi, We have received a request to make an account on your email adress \n This is your account activision code : {code} \n If this was not your request please ignore this message. \n Please avoid from sharing this message with anyone \n Thank you for your time . \t AB Group"
    send_mail(subject,message,"AB Group",[user.email],fail_silently=False)
    cowndown=True
    return(redirect("account:account_activator_view",username,cowndown))


"""
    This view will call code_sender function and check the code that will provide by user
"""
def account_activator_view(request,username,countdown=False):
    account=get_object_or_404(User,username=username)
    js_count=json.dumps(countdown)
    if(request.method=="POST"):
        form=account_activator(data=request.POST)
        if(form.is_valid()):
            code=form.cleaned_data["code"]
            #if(user.profile.code_limit)
            now=timezone.now()
            print(f"\n\n\n {now}  --- {account.profile.code_limit_time} \n\n\n")
            if(now > account.profile.code_limit_time):

                messages.error(request,"The activation code is expired.")
            else:    
                if(code==account.profile.code):
                    account.is_active=True 
                    account.save()
                    messages.success(request,"Account activated successfully.Now you can login into your account.")
                else:
                    messages.error(request,"The inserted activation code is not right.")
    else:
        form=account_activator()  
    return(render(request,"account/registration/account_activator.html",{"account":account,"form":form,"countdown":js_count}))


class CreateUserView(generics.CreateAPIView):
    serializer_class=UserCreationSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES


class TokenLogin(ObtainAuthToken):
    serializer_class=TokenSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES


class UserUpdateInfoView(generics.RetrieveUpdateAPIView):
    serializer_class=UserInfoUpdateSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES
    queryset=get_user_model().objects.all()
    permission_classes=(IsAuthenticated,)
    authentication_classes=(authentication.TokenAuthentication,)

    def get_object(self):
        return self.request.user
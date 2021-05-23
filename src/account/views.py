from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .forms import login_form,register_form
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from .utils import database_checker
from django.views.generic import FormView,TemplateView
from django.urls import reverse
from django.contrib.auth.views import  PasswordResetView


def login_view(request):
    if(request.method=="POST"):
        form=login_form(data=request.POST)
        if(form.is_valid()):
            cd=form.cleaned_data 
            user=authenticate(username=cd["username"],password=cd["password"])
            if(user):
                if(user.is_active):
                    login(request,user)
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
                return(("account:login_view"))
    else:
        form=register_form()
    return(render(request,"account/register_page.html",{"form":form}))


  
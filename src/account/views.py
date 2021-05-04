from django.shortcuts import render,redirect 
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .forms import login_form
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe


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
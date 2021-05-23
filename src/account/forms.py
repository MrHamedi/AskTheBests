from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import *


class login_form(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    
class register_form(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':"register-form-field"}))
    password2=forms.CharField(widget=forms.PasswordInput,label="Enter password again")

    class Meta:
        model=User
        fields=("username","email")

    def clean(self):
        cd=self.cleaned_data     
        if(len(cd["password"]) < 8 or cd["password"].isalpha() or cd["password"].isdigit()):
            raise(forms.ValidationError("Password must at least contain 8 characters include alphabets and numbers! "))
        if(cd["password"] != cd["password2"]):
            raise(forms.ValidationError("Passwords does not match!!!"))
        return(cd)


from django import forms 


class login_form(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    
class register_form(forms.Form):
    username=forms.CharField(max_length=50)
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':"register-form-field"}))
    password2=forms.CharField(widget=forms.PasswordInput,label="Enter password again")

    def clean(self):
        cd=self.cleaned_data     
        if(len(cd["password"]) < 8 or cd["password"].isalpha() or cd["password"].isdigit()):
            raise(forms.ValidationError("Password must at least contain 8 characters include alphabets and numbers! "))
        if(cd["password"] != cd["password2"]):
            raise(forms.ValidationError("Passwords does not match!!!"))
        return(cd)


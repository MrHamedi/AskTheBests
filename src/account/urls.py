from django.urls import path,include,reverse_lazy
from .views import login_view,logout_view,register_view
from django.contrib.auth.views import PasswordChangeView, PasswordResetCompleteView,PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView
from  .forms import PasswordChangeForm 

app_name="account" 

urlpatterns = [
    path("login/",login_view,name="login_view"),
    path("logout/",logout_view,name="logout_view"),
    path("register/",register_view,name="register_view"),
    path("password_change/",PasswordChangeView.as_view(template_name="account/password_change.html"),name="password_change_view"),
	path("password_reset/",PasswordResetView.as_view(template_name ='account/registration/password_reset.html',email_template_name = 'account/registration/password_reset_email.html',success_url=reverse_lazy('account:password_reset_done')),name="password_reset_view"),
    path("password_reset_confirm/",PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path("password_reset_done/",PasswordResetDoneView.as_view(template_name="account/registration/password_reset_done.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",PasswordResetConfirmView.as_view(template_name="account/registration/password_reset_confirm_form.html",success_url=reverse_lazy("account:password_reset_complete")),name='password_reset_confirm'),
    path("password-reset-completed/",PasswordResetCompleteView.as_view(template_name="account/registration/password_reset_complete.html"),name="password_reset_complete"),
]

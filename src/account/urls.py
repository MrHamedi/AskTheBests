from django.urls import path,include,reverse_lazy,reverse
from .views import login_view,logout_view,register_view,account_activator_view,code_sender_view
from django.contrib.auth.views import PasswordChangeView, PasswordResetCompleteView,PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView,PasswordChangeDoneView

app_name="account" 

urlpatterns = [
    path("login/",login_view,name="login_view"),
    path("logout/",logout_view,name="logout_view"),
    path("register/",register_view,name="register_view"),
    path("account_activator/email_sender/<str:username>/",code_sender_view,name="account_activator_sender"),
    path("account_activator/<str:username>/",account_activator_view,name="account_activator_view"),
    path("account_activator/<str:username>/<str:countdown>/",account_activator_view,name="account_activator_view"),
    path("account_activator/email_sender/<str:username>/",code_sender_view,name="account_activator_sender"),
    path("password_change/",PasswordChangeView.as_view(template_name="account/password_change.html",success_url=reverse_lazy("account:password_change_done")),name="password_change_view"),
	path("password_reset/",PasswordResetView.as_view(template_name ='account/registration/password_reset.html',email_template_name = 'account/registration/password_reset_email.html',success_url=reverse_lazy('account:password_reset_done')),name="password_reset_view"),
    path("password_reset_confirm/",PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path("password_reset_done/",PasswordResetDoneView.as_view(template_name="account/registration/password_reset_done.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",PasswordResetConfirmView.as_view(template_name="account/registration/password_reset_confirm_form.html",success_url=reverse_lazy("account:password_reset_complete")),name='password_reset_confirm'),
    path("password-reset-completed/",PasswordResetCompleteView.as_view(template_name="account/registration/password_reset_complete.html"),name="password_reset_complete"),
    path("password_change_done/",PasswordChangeDoneView.as_view(template_name="account/registration/password_change_done.html"),name="password_change_done"),
]

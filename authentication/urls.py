# Django
from django.urls import path
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView)

# local Django
from authentication import views
from authentication.views import anonymous_required
from authentication.forms import EmailValidationOnForgotPassword
from AlumniPortal import settings

app_name = 'authentication'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',
         anonymous_required(
             LoginView.as_view(
                 template_name='authentication/login.html'
             )
         ),
         name='login_process'),
    path('logout/',
         LogoutView.as_view(template_name='HomePage/HomePage.html'),
         name='logout_process'),
    path('password_reset/',
         PasswordResetView.as_view(email_template_name='authentication/password_reset_email.html',
                                   template_name='authentication/password_reset_form.html',
                                   success_url='done/',
                                   form_class=EmailValidationOnForgotPassword,
                                   subject_template_name='authentication/password_reset_subject.txt',
                                   from_email=settings.EMAIL_HOST_USER
                                   ),
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name='authentication/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name= 'authentication/password_change_form.html',
             success_url='/authentication/reset/complete/'
         ),
         name='password_reset_confirm'),
    path('reset/complete/',
         PasswordResetCompleteView.as_view(
             template_name='authentication/password_reset_complete.html'
         ),
         name='password_reset_complete'
         ),
    path('change-password/',
         PasswordChangeView.as_view(success_url='done/'),
         name='password_change'),
    path('change-password/done/',
         PasswordChangeDoneView.as_view(
             template_name='authentication/password_change_done.html'
         ),
         name='password_change_done'),
]

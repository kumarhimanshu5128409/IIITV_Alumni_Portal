from django.urls import path
from .views import AlumniSignupView
from registration import  views
from django.conf.urls import include, url
app_name = 'registration'

urlpatterns = [
    path('',AlumniSignupView.as_view(),name='signup_alumni'),
    url(r'^signup/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/'r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate,name='activate'),
]


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import AboutUs,ContactUs,NotAllowed,RegistrationEmailError

app_name='pages'

urlpatterns = [
    path('about_us/', AboutUs, name='about_us'),
    path('contact_us/', ContactUs, name='contact_us'),
    path('error/', NotAllowed, name='not_allowed'),
    path('server_error/', RegistrationEmailError, name='RegistrationEmailError')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += staticfiles_urlpatterns()


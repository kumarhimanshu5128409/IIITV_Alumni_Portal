from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('HomePage.urls')),
    path('post/',include('posts.urls')),
    path('alumni/',include('alumni.urls')),
    path('gallery/',include('gallery.urls')),
    path('community/',include('community.urls')),
    path('register/',include('registration.urls')),
    path('authentication/', include('authentication.urls')),
    path('pages/', include('pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += staticfiles_urlpatterns()


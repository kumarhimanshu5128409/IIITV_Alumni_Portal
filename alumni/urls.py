# Django
from django.urls import path

# local Django
from alumni import views
from .views import (AlumniUpdateView, ProfileView)

app_name = 'alumni'

urlpatterns = [
    path('profile/<int:alumni_id>',ProfileView.as_view(),name='profile'),
    path('edit/<int:alumni_id>',AlumniUpdateView.as_view(),name='edit'),
]


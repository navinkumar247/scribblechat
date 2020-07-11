from django.urls import path, re_path
from .views import register


app_name = 'profiles'

urlpatterns = [
    path('', register, name='register'),
]

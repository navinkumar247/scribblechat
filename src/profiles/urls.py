from django.urls import path, re_path
from .views import register, ThankYouPage
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

app_name = 'profiles'

urlpatterns = [
    path('', register, name='register'),
    path('logged-out/', LogoutView.as_view(), name='logout'),
    path('thankyou/', ThankYouPage.as_view(), name='thankyou'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

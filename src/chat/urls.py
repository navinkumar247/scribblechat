from django.urls import path, re_path
from .views import index, room, FriendRequest, AcceptRequest
from django.conf.urls.static import static
from django.conf import settings

app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('friendrequest/<username>', FriendRequest.as_view(), name='friendrequest'),
    path('acceptrequest/<username>', AcceptRequest.as_view(), name='acceptrequest'),
    re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

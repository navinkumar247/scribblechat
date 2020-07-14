from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from profiles.models import Relationship
@login_required
def index(request):

    context = {
        'friends': request.user.profile.get_friends()
    }
    return render(request, 'chat/index.html', context)


@login_required
def room(request, room_name):
    
    message_receiver = get_message_receiver(request, room_name)

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'friends': request.user.profile.get_friends(),
        'message_receiver': message_receiver,
    })
@login_required
def get_message_receiver(request, room_name):
    relation = Relationship.objects.get(slug = room_name)
    
    if relation.receiver.user != request.user:
        message_receiver = relation.receiver
    else:
        message_receiver = relation.sender
    return message_receiver
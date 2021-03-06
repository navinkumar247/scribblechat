from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from profiles.models import Relationship, Profile
from profiles.forms import ProfileUpdateForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import User

@login_required(login_url='profiles:register')
def index(request):

    # EDIT PROFILE CODE
    user_profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        if 'edit_profile' in request.POST:
            update_form = ProfileUpdateForm(data = request.POST, files= request.FILES, instance=user_profile)
            if update_form.is_valid():
                profile = update_form.save(commit=False)
                if 'image' in request.FILES:
                    profile.image = request.FILES['image']
                update_form.save()
    update_form = ProfileUpdateForm(instance=user_profile)

    # GET CONTACT SEARCH DATA
    all_relations = request.user.profile.get_friends() # Get all relationship objects
    searched_contacts, searched_my_contacts = get_contacts(request)
    friends = get_friends_profiles_from_relations(request, all_relations)
    online_relations, offline_relations = get_online_users(request, friends)
    if searched_my_contacts:
        online_relations = []
        offline_relations = []
    received_requests, sent_requests = request.user.profile.get_pending_requests()

    context = {
        'friends': all_relations,
        'online_friends': online_relations,
        'offline_friends': offline_relations,
        'update_form':update_form,
        'contacts': searched_contacts,
        'searched_contacts': searched_my_contacts,
        'received_requests':received_requests,
        'sent_requests':sent_requests,
    }
    return render(request, 'chat/index.html', context)

def get_contacts(request):
    
    searched_contacts = []
    searched_my_contacts = []
    if request.method == 'GET':
        if 'search_my_contacts' in request.GET:
            username_contains = request.GET.get('username_contains')
            if username_contains != '' and username_contains is not None:
                searched_my_contacts = request.user.profile.get_searched_friends(username_contains)
        elif 'search_new_contacts' in request.GET:
            username_contains = request.GET.get('username_contains')
            if username_contains != '' and username_contains is not None:
                searched_contacts = Profile.objects.filter(user__username__icontains = username_contains)
                # contacts = serializers.serialize('json', searched_contacts)
                # return JsonResponse({"contacts":contacts}, safe=False)
    return searched_contacts, searched_my_contacts

def get_friends_profiles_from_relations(request, all_relations):
    friends = []
    for item in all_relations:
        if item.sender != request.user.profile:
            friends.append(item.sender)
        elif item.receiver != request.user.profile:
            friends.append(item.receiver)
    return friends

def get_online_users(request, friends):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    
    all_online_users = User.objects.filter(id__in = uid_list)
    online_friends = all_online_users.filter(profile__in = friends)
    offline_friends = []

    for friend in friends:
        if friend.user not in online_friends:
            offline_friends.append(friend.user)
    
    online_friends_relation = Relationship.objects.filter(
        Q(sender__user__in = online_friends, receiver = request.user.profile)|
        Q(sender=request.user.profile, receiver__user__in = online_friends)
        )
    offline_friends_relation = Relationship.objects.filter(
        Q(sender__user__in = offline_friends, receiver = request.user.profile)|
        Q(sender=request.user.profile, receiver__user__in = offline_friends)
        )
    return online_friends_relation, offline_friends_relation

@login_required(login_url='profiles:register')
def room(request, room_name):
    
    message_receiver = get_message_receiver(request, room_name)
    # GET CONTACT SEARCH DATA
    all_relations = request.user.profile.get_friends() # Get all relationship objects
    searched_contacts, searched_my_contacts = get_contacts(request)
    friends = get_friends_profiles_from_relations(request, all_relations)
    online_relations, offline_relations = get_online_users(request, friends)
    if searched_my_contacts:
        online_relations = []
        offline_relations = []
    received_requests, sent_requests = request.user.profile.get_pending_requests()

    context = {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'message_receiver': message_receiver,
        'friends': friends,
        'contacts': searched_contacts,
        'searched_contacts': searched_my_contacts,
        'online_friends': online_relations,
        'offline_friends': offline_relations,
        'received_requests':received_requests,
        'sent_requests':sent_requests,
    }

    return render(request, 'chat/room.html', context)


def get_message_receiver(request, room_name):
    relation = Relationship.objects.get(slug = room_name)
    
    if relation.receiver.user != request.user:
        message_receiver = relation.receiver
    else:
        message_receiver = relation.sender
    return message_receiver

class FriendRequest(RedirectView, LoginRequiredMixin):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('chat:index')

    def get(self, *args, **kwargs):
        username = self.kwargs.get('username')

        profile1  = get_object_or_404(Profile, user = self.request.user)
        profile2 = get_object_or_404(Profile, user__username = username)

        relation = Relationship.objects.filter(Q(sender=profile1, receiver=profile2)|Q(sender=profile2,  receiver=profile1))

        if not relation.exists():
            relation = Relationship.objects.create(sender = profile1, receiver = profile2, status = 'sent')
            relation.save()
        elif relation.exists() and relation[0].status == 'sent':
            relation[0].delete()
        elif relation.exists() and relation[0].status == 'accepted':
            relation[0].delete()
        return super().get(*args, **kwargs)

class AcceptRequest(RedirectView, LoginRequiredMixin):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('chat:index')

    def get(self, *args, **kwargs):
        username = self.kwargs.get('username')
        profile1  = get_object_or_404(Profile, user = self.request.user)
        profile2 = get_object_or_404(Profile, user__username = username)
        relation = Relationship.objects.filter(Q(sender=profile1, receiver=profile2)|Q(sender=profile2,  receiver=profile1))
        if not relation.exists():
            relation = Relationship.objects.create(sender = profile1, receiver = profile2, status = 'sent')
            relation.save()
        elif relation.exists() and relation[0].receiver == profile1:
            relation = relation[0]
            relation.status = 'accepted'
            relation.save()
        return super().get(*args, **kwargs)

    
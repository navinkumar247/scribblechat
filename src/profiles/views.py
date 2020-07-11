from django.shortcuts import render
from .models import Profile, Relationship
from .forms import UserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.

def register(request):
    if request.method == 'POST':
        
        if 'registration' in request.POST:
            user_form = UserForm(data=request.POST)
            profile_form = ProfileForm(data=request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                messages.success(request, "Registration Succesful")
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                if 'image' in request.FILES:
                    profile.image = request.FILES['image']
                profile.save()
            elif not (user_form.is_valid() and profile_form.is_valid()):
                messages.error(request, "Invalid details / Either username or email id already registered")
        elif 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('chat:index'))
            else:
                messages.error(request, 'Invalid credentials / User not active')

    user_form = UserForm()
    profile_form = ProfileForm()

    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
    }

    return render(request, 'profiles/register.html', context)
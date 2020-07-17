from django.shortcuts import render
from .models import Profile, Relationship
from .forms import UserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView

# Create your views here.

def register(request):
    if request.method == 'POST':
        
        if 'registration' in request.POST:
            user_form = UserForm(data=request.POST)
            profile_form = ProfileForm(data=request.POST, files=request.FILES)

            if user_form.is_valid() and profile_form.is_valid():
                
                user = user_form.save() #Password is hashed by default. Need not do a set_password again

                profile = profile_form.save(commit=False)
                profile.user = user
                if 'image' in request.FILES:
                    profile.image = request.FILES['image']
                profile.save()
                messages.success(request, "Registration Succesful")

            elif not (user_form.is_valid() and profile_form.is_valid()):
                messages.error(request, "Invalid details / Either username or email id already registered")
            user_form = UserForm()
            profile_form = ProfileForm()

        elif 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('chat:index'))
                else:
                    messages.error(request, 'User not active')    
            else:
                messages.error(request, 'Invalid credentials')

    user_form = UserForm()
    profile_form = ProfileForm()

    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
    }

    return render(request, 'profiles/register.html', context)

class ThankYouPage(TemplateView):
    template_name = "profiles/thankyou.html"

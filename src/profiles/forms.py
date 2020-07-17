from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserForm(UserCreationForm):
    username = forms.CharField(label= '', widget=forms.TextInput( attrs={'Placeholder' : 'Username',} ))
    password1 = forms.CharField(label= '',  widget=forms.PasswordInput(attrs = {'Placeholder': 'Password',}))
    password2 = forms.CharField(label= '',  widget=forms.PasswordInput(attrs = {'Placeholder':'Confirm Password',} ))
    class Meta:
        model = User
        fields = ('username', 'password1','password2')

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label= '', widget=forms.TextInput(attrs = {'Placeholder': 'Email'}))
    image = forms.ImageField(label= '', required=False, widget=forms.ClearableFileInput(attrs = {'Placeholder': 'Profile Picture', 'class':'image'}), )
    bio  = forms.CharField(label= '', required=False,  widget=forms.Textarea(attrs = {'Placeholder': 'Tell something about yourself', 'rows':6,'cols':30}))
    class Meta:
        model = Profile 
        fields = ("email",'image','bio')

class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ("email","image","bio")


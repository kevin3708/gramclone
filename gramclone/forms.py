from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.files.images import get_image_dimensions

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'image_name', 'caption')
         
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user','post']
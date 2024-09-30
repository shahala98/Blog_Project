from django import forms
from django.contrib.auth.models import User
from .models import Profile , Comment,Blog
from django.contrib.auth.forms import UserCreationForm



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'phone', 'about', 'profile_image', 'id_proof']

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']

class CommentForm(forms.ModelForm):
     comment = forms.CharField(
        max_length=100,
        required=False,
        label="comments",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
     class Meta:
         model = Comment
         fields = ['comment']


class BlogForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        required=True,
        label="Title",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        required=True,
        label="Content",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
    )
    blog_images = forms.ImageField(
        required=False,
        label="Blog Image",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    status = forms.ChoiceField(
        choices=Blog.STATUS_CHOICES,
        required=True,
        label="Status",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'blog_images', 'status']


class BlogImageForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['blog_image']



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
    

      
        
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )

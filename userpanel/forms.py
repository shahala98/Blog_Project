from django import forms
from django.contrib.auth.models import User
from adminpanel.models import Profile , Comment,Blog
from django.contrib.auth.forms import PasswordChangeForm




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
    blog_image = forms.ImageField(
        required=False,
        label="Blog Images",
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
        fields = ['title', 'content', 'blog_image', 'status']

# class BlogImageForm(forms.ModelForm):
#     class Meta:
#         model = Blog
#         fields = ['blog_image']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Current Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm New Password"
    )
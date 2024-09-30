from django import forms
from django.contrib.auth.models import User
from .models import  Comment,Blog

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
        fields = ['title', 'content', 'blog_image', 'status']

class BlogImageForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['blog_image']

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

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from PIL import Image

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Username"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )
    id_proof = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="ID Proof"
    )
    profile_image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Profile Image"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'id_proof', 'profile_image']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        profile_image = cleaned_data.get("profile_image")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        if profile_image:
            try:
                img = Image.open(profile_image)
                max_width, max_height = 800, 800
                if img.width > max_width or img.height > max_height:
                    raise ValidationError(f"Image dimensions should not exceed {max_width}x{max_height} pixels.")
            except IOError:
                raise ValidationError("Invalid image format")

        return cleaned_data

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

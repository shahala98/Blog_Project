from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from .forms import LoginForm, RegistrationForm
from django.contrib import messages

# Create your views here.

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set the user's password
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')  # Ensure this URL name exists
        else:
            messages.error(request, 'There were errors in your form. Please correct them and try again.')
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = RegistrationForm()
    return render(request, 'sitevisitor/registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('admin_home')  # Redirect to the home page or another page
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'sitevisitor/login.html', {'form': form})


def home(request):
    return render(request, 'sitevisitor/home.html')

def forgot_password(request):
    return render(request, 'sitevisitor/forgot_password.html')

def reset_password(request):
    return render(request, 'sitevisitor/reset_password.html')

def otp(request):
    return render(request, 'sitevisitor/otp.html')

def user_home(request):
    return render(request, 'userpanel/user_home.html')

def admin_home(request):
    logged_user =request.user
    return render(request, 'adminpanel/admin_home.html',{'logged_user':logged_user})

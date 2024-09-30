from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, RegistrationForm, ProfileForm
from django.contrib import messages
from adminpanel .models import Blog

# Create your views here.


# def home(request):
#     # Exclude blogs authored by users whose profiles have been deleted
#     blogs = Blog.objects.filter(author__profile__isnull=False)  # Only include blogs where the author's profile exists
#     return render(request, 'sitevisitor/home.html', {'blogs': blogs})



def home(request):
    # Exclude blogs authored by users whose profiles have been deleted and also exclude drafts
    blogs = Blog.objects.filter(
        author__profile__isnull=False,  # Only include blogs where the author's profile exists
        status='published'  # Only include blogs with 'published' status
    )
    return render(request, 'sitevisitor/home.html', {'blogs': blogs})



def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            

            profile = profile_form.save(commit=False)
            profile.user= user
            profile.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login') 
        else:
            messages.error(request, 'cannot register ,please correct error below.')
            print(form.errors) 
    else:
        form = RegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'sitevisitor/registration.html', {'form': form , 'profile_form' : profile_form})



# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, 'Login successful.')
#                 return redirect('user_home') 
#             else:
#                 messages.error(request, 'Invalid username or password.')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = LoginForm()
#     return render(request, 'sitevisitor/login.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Check if the user has an associated profile
                if hasattr(user, 'profile'):
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    return redirect('user_home')
                else:
                    messages.error(request, 'This account is no longer active.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'sitevisitor/login.html', {'form': form})


def admin_login(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('home') 

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_staff:
                return redirect('admin_home')  
            else:
                return redirect('admin_home')  
    else:
        form = AuthenticationForm()
    
    return render(request, 'adminpanel/admin_login.html', {'form': form})


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



def custom_404_view(request, exception=None):
    return render(request, 'sitevisitor/404.html', status=404)



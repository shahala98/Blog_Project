
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Blog ,Profile,Comment
from django.contrib import messages
from .forms import LoginForm,CommentForm
       

# Create your views here.

def admin_home(request):
    latest_blog = Blog.objects.order_by('-created_at').first()
    context = {
        'latest_blog': latest_blog,
    }
    return render(request, 'adminpanel/admin_home.html', context)


def admin_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('admin_home')                
            else:
                messages.error(request, 'Invalid username or password')
    return render(request, 'adminpanel/admin_login.html', {'form': form})
      


def blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    last_three_blogs = Blog.objects.exclude(id=blog_id).order_by('-created_at')  # Excludes the current blog
    context = {
        'blog': blog,
        'last_three_blogs': last_three_blogs,
    }
    return render(request, 'adminpanel/blog_view.html', context)






# def user_list(request):
#     users = User.objects.all()
#     return render(request, 'adminpanel/user_list.html', {'users': users})

def user_list(request):
    # Filter users who still have an associated profile
    users = User.objects.filter(profile__isnull=False)
    return render(request, 'adminpanel/user_list.html', {'users': users})


def admin_blog_list(request):
    visible_blogs = Blog.objects.filter(visible=True)
    hidden_blogs = Blog.objects.filter(visible=False)
    context = {
        'visible_blogs': visible_blogs,
        'hidden_blogs': hidden_blogs
    }
    return render(request, 'adminpanel/admin_blog_list.html', context)


def view_user(request):
    user_id = request.GET.get('id')

    if user_id:
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        blogs = Blog.objects.filter(author=user)  
        context = {
            'user': user,
            'profile': profile,
            'blogs': blogs
        }
        return render(request, 'adminpanel/view_user.html', context)
    else:
        users = User.objects.all()
        return render(request, 'adminpanel/view_user.html', {'users': users})


def reset_password(request):
    return render(request, 'adminpanel/reset_password.html')


def edit_blog(request):
    return render(request, 'adminpanel/edit.html')



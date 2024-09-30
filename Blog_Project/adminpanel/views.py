

# Create your views here.

from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from .models import Blog,Profile

def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda user: user.is_staff)(view_func)
    return decorated_view_func


def blog_view(request):
    blogs = Blog.objects.all().order_by('-created_at')
    context = {
        'blogs': blogs
    }
    return render(request, 'adminpanel/blog_list.html', context)

from django.contrib.auth.decorators import login_required


def user_list(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'adminpanel/user_list.html', context)



def blog_list(request):
    return render(request, 'adminpanel/blog_list.html')

def view_user(request):
    user_id = request.GET.get('id') 

    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        users = User.objects.all()
        return render(request, 'adminpanel/view_user.html', {'users': users})

    return render(request, 'adminpanel/view_user.html', {'user': user})

def reset_password(request):
    return render(request, 'adminpanel/reset_password.html')


def admin_home(request):
    return render(request, 'adminpanel/admin_home.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import HttpResponseRedirect
from .models import Blog, Comment, Profile
from .forms import BlogForm, CommentForm, BlogImageForm,ProfileForm,ProfilePhotoForm,RegistrationForm,LoginForm
from django.contrib import messages
from django.contrib.auth import views as auth_views

def user_home(request):
    blogs = Blog.objects.all() 
    context = {
        'blogs': blogs,
        
    }
    return render(request, 'userpanel/user_home.html', context)


# Blog view


def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')  # Redirect after saving
    else:
        form = BlogForm()
    return render(request, 'userpanel/add_blog.html', {'form': form})


def default_blog_view(request):
    blogs = Blog.objects.all()
    return render(request, 'userpanel/default_blog_view.html', {'blogs': blogs})
    


def view_blog(request):
    
        blog = get_object_or_404(Blog, )
        comments = Comment.objects.filter(blog=blog).order_by('-created_at')

        if request.method == 'POST':
            if 'comment_submit' in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.blog = blog
                    new_comment.author = request.user
                    new_comment.save()
                    return HttpResponseRedirect(request.path_info) 
            elif 'image_submit' in request.POST:
                image_form = BlogImageForm(request.POST, request.FILES, instance=blog)
                if image_form.is_valid():
                    image_form.save()
                    return HttpResponseRedirect(request.path_info)  
            else:
                edit_form = BlogForm(instance=blog)  
        else:
            comment_form = CommentForm()
            image_form = BlogImageForm(instance=blog)
            edit_form = BlogForm(instance=blog)  

        context = {
            'blog': blog,
            'comments': comments,
            'comment_form': comment_form,
            'image_form': image_form,
            'edit_form': edit_form,
        }
        return render(request, 'userpanel/view_blog.html', context)
    
    
    

def my_blog(request):
    blogs = Blog.objects.order_by('-created_at')[:5]  
    context = {'blogs': blogs}
    return render(request, 'userpanel/my_blog.html', context)



def blog_list(request):
    blogs = Blog.objects.all() 
    context = {
        'blogs': blogs,
    }
    return render(request, 'userpanel/blog_list.html', context)




def delete_blog(request,blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == 'POST':
        
        blog.delete()
        messages.success(request, 'Blog post deleted successfully.')
        return redirect('blog_list')  

    return render(request, 'userpanel/delete_blog.html', {'blog': blog})



def edit_blog(request, blog_id):
    try:
        blog = get_object_or_404(Blog, pk=blog_id)
        
        if request.method == 'POST':
            form = BlogForm(request.POST, instance=blog)
            if form.is_valid():
                form.save()
                return redirect('view_blog', blog_id=blog.id) 
        else:
            form = BlogForm(instance=blog)
        
    except Blog.DoesNotExist:
        return redirect('view_blog')  
    
    return render(request, 'userpanel/edit_blog.html', {'form': form})



def blog_details(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = Comment.objects.filter(blog=blog)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('blog_details', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'userpanel/blog_details.html', {'blog': blog, 'comments': comments, 'form': form})

# comment view

def add_comment(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('blog_details',  pk=comment.blog.id)
        else:
            messages.error(request, 'Error adding comment. Please check the form.')
    else:
        form = CommentForm()
    
    return render(request, 'userpanel/add_comment.html', {'form': form})



def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        blog_id = comment.blog.id 
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('blog_details',  pk=comment.blog.id)
    
    
    context = {
        'blog': comment.blog 
    }
    return render(request, 'userpanel/delete_comment.html', context)

   
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog_details',  pk=comment.blog.id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'userpanel/edit_comment.html', {'form': form, 'comment': comment})

# profile view


def view_profile(request):
    print(f"Current user: {request.user}")
    try:
        user_profile = Profile.objects.get(user=request.user)
        print(f"User profile found: {user_profile}")
    except Profile.DoesNotExist:
        print("No profile found for this user.")
        user_profile = None
    return render(request, 'userpanel/view_profile.html', {'profile': user_profile})



def add_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  
            profile.save()
            return redirect('view_profile') 
    else:
        form = ProfileForm()
    
    return render(request, 'userpanel/add_profile.html', {'form': form})


def edit_profile(request):
    profile = get_object_or_404(Profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')  
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'userpanel/edit_profile.html', {'form': form})


def delete_profile(request):
    profile = get_object_or_404(Profile, )

    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Profile deleted successfully.')
        return redirect('view_profile')  
    return render(request, 'userpanel/delete_profile.html', {'profile': profile})



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# create morethan 1 profile




def reset_password(request):
    return render(request, 'userpanel/reset_password.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


# user registreation
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set the user's password
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('user_login')  # Ensure this URL name exists
        else:
            messages.error(request, 'There were errors in your form. Please correct them and try again.')
    else:
        form = RegistrationForm()
    return render(request, 'userpanel/user_register.html', {'form': form})



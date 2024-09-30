from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from adminpanel.models import Blog, Comment, Profile
from .forms import BlogForm, CommentForm, ProfileForm ,ProfilePhotoForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm
from django.http import HttpResponseForbidden
       

# def user_home(request):
#     if request.user.is_authenticated:
#         blogs = Blog.objects.filter(status='published')
#     else:
#         blogs = Blog.objects.none() 

#     return render(request, 'userpanel/user_home.html', {
#         'blogs': blogs
#     })

def user_home(request):
    if request.user.is_authenticated:
        # Exclude blogs authored by users whose profiles have been deleted
        blogs = Blog.objects.filter(status='published', author__profile__isnull=False) # dont shw dleted blogs
    else:
        blogs = Blog.objects.none() 

    return render(request, 'userpanel/user_home.html', {
        'blogs': blogs
    })

# Blog views
@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(blog=blog).order_by('-created_at')
    
    if request.method == 'POST':
        form = CommentForm(request.POST) #comment section
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('view_blog', blog_id=blog.id)
    else:
        form = CommentForm()

    return render(request, 'userpanel/view_blog.html', {'blog': blog, 'comments': comments, 'form': form})


@login_required
def hide_comments(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if blog.author != request.user:
        messages.error(request, "You are not authorized to hide comments for this blog.")
        return redirect('view_blog', blog_id=blog.id)
    
    comments = blog.comment_set.all() 
    comments.update(visible=False)
    messages.success(request, "Comments have been hidden successfully.")
    return redirect('view_blog', blog_id=blog.id)



@login_required
def show_comments(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author != request.user:
        messages.error(request, "You are not authorized to show comments for this blog.")
        return redirect('view_blog', blog_id=blog.id)
    
    comments = blog.comment_set.all()
    comments.update(visible=True)
    messages.success(request, "Comments are now visible.")
    return redirect('view_blog', blog_id=blog.id)



@login_required
def my_blog(request):
    blogs = Blog.objects.order_by('-created_at')[:5]
    context = {'blogs': blogs}
    return render(request, 'userpanel/my_blog.html', context)


@login_required
def hide_blog(request, blog_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to hide a blog.')
        return redirect('login')

    blog = get_object_or_404(Blog, id=blog_id)

    if blog.author == request.user or request.user.is_superuser:
        blog.status = 'hidden'
        blog.visible = False
        blog.save()
        messages.success(request, 'Blog hidden successfully.')
    else:
        messages.error(request, 'You do not have permission to hide this blog.')

    return redirect('blog_list')


@login_required
def show_blog(request, blog_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to show a blog.')
        return redirect('login')

    blog = get_object_or_404(Blog, id=blog_id)

    if blog.author == request.user or request.user.is_superuser:
        blog.status = 'published'
        blog.visible = True
        blog.save()
        messages.success(request, 'Blog is now visible.')
    else:
        messages.error(request, 'You do not have permission to show this blog.')

    return redirect('blog_list')



@login_required
def publish_blog(request, blog_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to publish a blog.')
        return redirect('login')

    blog = get_object_or_404(Blog, id=blog_id)

    if blog.author == request.user or request.user.is_superuser:
        blog.status = 'published'
        blog.visible = True
        blog.save()
        messages.success(request, 'Blog published successfully.')
    else:
        messages.error(request, 'You do not have permission to publish this blog.')

    return redirect('blog_list')


# @login_required
# def blog_list(request):
#     if request.user.is_authenticated:
#         published_blogs = Blog.objects.filter(status='published')
#         hidden_blogs = Blog.objects.filter(status='hidden', author=request.user)
#         draft_blogs = Blog.objects.filter(status='draft', author=request.user)
#     else:
#         published_blogs = Blog.objects.filter(status='published')
#         hidden_blogs = Blog.objects.none()
#         draft_blogs = Blog.objects.none()

#     return render(request, 'userpanel/blog_list.html', {
#         'published_blogs': published_blogs,
#         'hidden_blogs': hidden_blogs,
#         'draft_blogs': draft_blogs
#     })
    
@login_required
def blog_list(request):
    if request.user.is_authenticated:
        # Exclude blogs authored by users whose profiles have been deleted
        published_blogs = Blog.objects.filter(status='published', author__profile__isnull=False)
        hidden_blogs = Blog.objects.filter(status='hidden', author=request.user, author__profile__isnull=False)
        draft_blogs = Blog.objects.filter(status='draft', author=request.user, author__profile__isnull=False)
    else:
        published_blogs = Blog.objects.filter(status='published', author__profile__isnull=False)
        hidden_blogs = Blog.objects.none()
        draft_blogs = Blog.objects.none()

    return render(request, 'userpanel/blog_list.html', {
        'published_blogs': published_blogs,
        'hidden_blogs': hidden_blogs,
        'draft_blogs': draft_blogs
    })


@login_required
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog post created successfully.')
            return redirect('blog_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogForm()
    return render(request, 'userpanel/add_blog.html', {'form': form})



@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this blog post.")
    
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully.")
            return redirect('view_blog', blog_id=blog.id)
        else:
            messages.error(request, "There was an error updating the blog post.")
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'userpanel/edit_blog.html', {'form': form})



@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this blog post.")
    
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog post deleted successfully.")
        return redirect('blog_list')
    
    return render(request, 'userpanel/delete_blog.html', {'blog': blog})



# Comment views
@login_required
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
            return redirect('blog_details', pk=comment.blog.id)
        else:
            messages.error(request, 'Error adding comment. Please check the form.')
    else:
        form = CommentForm()
    return render(request, 'userpanel/add_comment.html', {'form': form})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('view_blog', blog_id=comment.blog.id)
        else:
            messages.error(request, "There was an error updating the comment.")
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'userpanel/edit_comment.html', {'form': form})



@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    
    if request.method == "POST":
        blog_id = comment.blog.id
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('view_blog', blog_id=blog_id)
    
    return render(request, 'userpanel/delete_comment.html', {'comment': comment})

# Profile views


@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'userpanel/view_profile.html', {'user': user})



@login_required
def add_profile(request):
    if hasattr(request.user, 'profile'):
        return redirect('view_profile')

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



@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('view_profile', user_id=request.user.id)  # Pass the user_id
        else:
            messages.error(request, 'There were errors in your form. Please correct them and try again.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'userpanel/edit_profile.html', {'form': form})



# @login_required
# def delete_profile(request):
#     profile = get_object_or_404(Profile, user=request.user)
#     if request.method == 'POST':
#         profile_id = request.POST.get('profile_id')
#         if profile_id:
#             try:
#                 profile = get_object_or_404(Profile, id=profile_id)
#                 profile.delete()
#                 messages.success(request, 'Profile deleted successfully.')
#             except Profile.DoesNotExist:
#                 messages.error(request, 'Profile not found.')
#         else:
#             messages.error(request, 'No profile ID provided.')

#         return redirect('login')   
#     return render(request, 'userpanel/delete_profile.html')

def delete_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            user = request.user
            profile.delete()  # Deletes the profile and associated blogs
            logout(request)  # Logs out the user
            messages.success(request, 'Your profile and all associated blogs have been deleted.')
            return redirect('login')  # Redirect to the login page

        elif 'cancel' in request.POST:
            messages.info(request, 'Profile deletion canceled.')
            return redirect('view_profile', user_id=request.user.id)  # Pass user_id here

    return render(request, 'userpanel/delete_profile.html', {'profile': profile})



def upload_profile_photo(request):
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfilePhotoForm(instance=request.user.profile)
    return render(request, 'userpanel/view_profile.html', {'form': form})



def reset_password(request):
    return render(request, 'userpanel/reset_password.html')

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'userpanel/reset_password.html'


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')
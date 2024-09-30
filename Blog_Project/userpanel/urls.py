from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    user_home, view_profile, edit_profile, add_blog, edit_blog, view_blog,
    my_blog, blog_list, reset_password, blog_details, delete_blog, add_comment, delete_comment,
    edit_comment, add_profile, delete_profile, user_logout, register,
)

urlpatterns = [
    path('', user_home, name='user_home'),
    path('add_blog/', add_blog, name='add_blog'),
    path('view_blog/',view_blog, name='view_blog'),
    path('my_blog/', my_blog, name='my_blog'),
    path('blog_list/', blog_list, name='blog_list'),
    path('reset_password/', reset_password, name='reset_password'),
    path('blog/<int:pk>/', blog_details, name='blog_details'),
    path('edit_blog/<int:blog_id>/', edit_blog, name='edit_blog'),
    path('delete_blog/<int:blog_id>/', delete_blog, name='delete_blog'),
    path('add_comment/<int:blog_id>/', add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('view_profile/', view_profile, name='view_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('add_profile/', add_profile, name='add_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('user_logout/', user_logout, name='user_logout'),
    path('user_register/', register, name='user_register'),
    path('login/', auth_views.LoginView.as_view(template_name='userpanel/login.html'), name='login'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
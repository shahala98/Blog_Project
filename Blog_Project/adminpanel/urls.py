from django.urls import path
from . views import (admin_home, user_list, view_user, blog_list, blog_view, reset_password,
                     )

urlpatterns = [
    path('', admin_home, name='admin_home'),
    path('user_list/', user_list, name='user_list'),
    path('view_user/', view_user, name='view_user'),
    path('bloglist/', blog_list, name='blog_list'),
    path('blog_view/', blog_view, name='blog_view'),
    path('reset_password/',reset_password, name='reset_password'),
    
]

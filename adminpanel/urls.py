from django.urls import path
from .views import (admin_home, user_list, view_user, admin_blog_list, blog_view, reset_password, admin_login,
                 
                    
                   )
app_name = 'adminpanel'
urlpatterns = [
    path('', admin_home, name='admin_home'),
    path('user_list/', user_list, name='user_list'),
    path('view_user/', view_user, name='view_user'),
    path('blogs/', admin_blog_list, name='blog_list'),
    # path('blog_view', blog_view, name='blog_view'),
    path('blog/<int:blog_id>/',blog_view, name='blog_view'),
    path('reset_password/', reset_password, name='reset_password'),
    path('admin_login/' , admin_login ,name= 'admin_login'),
   
]

from django.urls import path
from .views import home, login_view, registration, forgot_password, reset_password, otp, admin_home ,admin_login,custom_404_view

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('registration/', registration, name='registration'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/', reset_password, name='reset_password'),
    path('otp/', otp, name='otp'),
    path('adminpanel/home', admin_home, name='admin_home'),
    path('admin/login/', admin_login, name='admin_login'),
    path('404/', custom_404_view ,name= '404'),
     
]


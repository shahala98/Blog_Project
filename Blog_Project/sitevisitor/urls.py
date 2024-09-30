from django.urls import path
from . views import home, login_view, registration, forgot_password, reset_password, otp,admin_home 

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('registration/', registration, name='registration'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/', reset_password, name='reset_password'),
    path('otp/', otp, name='otp'),
    path('adminpanel/home', admin_home, name='admin_home'),
    
    ]
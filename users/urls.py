"""SiteProgramacaoParaMakers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from users.views import ActivateAccount

urlpatterns = [

    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/<str:username>', user_views.profile, name='profile_detail'),
    path('activate/<str:uidb64>/<str:token>',
        user_views.activate, name='activate'),
    
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',
                                                redirect_authenticated_user=True), 
                                                name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('ActivateAccount/',
         user_views.ActivateAccount,
         name='Account-activation'),
    
    path('email_used/',user_views.email_used, name='email_used'),
    path('victories/',user_views.victories, name='medals'),
    
    path('share/',user_views.share, name='share'),
]


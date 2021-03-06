"""url_shortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import home, shorten_url, goto_dashboard, register, redirect_to_original_url, shorten_customized_url, update_username, update_password, delete_account

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('shorten_url', shorten_url, name='shorten_url'),
    path('dashboard', goto_dashboard, name='goto_dashboard'),
    path('register', register, name='register'),
    path('shorten_customized_url', shorten_customized_url, name="shorten_dashboard_url"),
    path('update_username', update_username, name='update_username'),
    path('update_password', update_password, name='update_password'),
    path('delete_account', delete_account, name='delete_account'),
    path('login', 
        LoginView.as_view(template_name='url_shortener/login.html', redirect_authenticated_user=True), 
        name='login'),
    path('logout', 
        LogoutView.as_view(), 
        name='logout'),
    path('<slug:slug>', redirect_to_original_url)
]

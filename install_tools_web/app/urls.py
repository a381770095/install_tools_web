"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from app import urls as app_urls
from app import views

urlpatterns = [
    path('list/', views.list, name='list'),
    path('register/',views.register,name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('get_code/', views.get_code, name='get_code'),
    path('changepsd/', views.changepsd, name='changepsd'),
    path('addhost/', views.addhost, name='addhost'),
    path('addshell/', views.addshell, name='addshell'),
    path('delhost/', views.delhost, name='delhost'),
    path('delshell/', views.delshell, name='delshell'),
    path('runinstall/', views.runinstall, name='runinstall'),
    path('upfile/', views.upfile, name='upfile'),
]

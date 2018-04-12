"""business URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path

from . import views

from django.contrib.auth.views import (
    login, logout, 
    password_reset, password_reset_done,
    password_reset_confirm, password_reset_complete,
)

app_name = "accounts"
urlpatterns = [
   path('',views.dashboard, name="home"),
   path('login/',login,{'template_name':'accounts/index.html'}),
   path('logout/',logout,{'template_name':'accounts/logout.html'}),
   # path('logout/',views.logout_view, name="logout"),
   path('register/',views.registration,name="register"),
   path('sentiment/<int:primary_id>',views.sentiment, name='sentiment'),
   path('attachments/<int:primary_id>',views.attachments, name="attachments"),
   path('results/<int:primary_id>',views.data_processing, name='analysis')
]

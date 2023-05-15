"""
URL configuration for twgo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path  # include
from twgobackend import views
from twgobackend.views import BalanceView, UserUpdateView

urlpatterns = [
    # path("twgobackend/", include("twgobackend.urls")),
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('register-user/', views.create_custom_user, name='registerUser'),
    path('create-admin/', views.create_custom_admin, name='registerAdmin'),
    path('userlogin/', views.login_custom_user, name='userlogin'),
    path('adminlogin/', views.login_custom_admin, name='adminlogin'),
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('balance/', BalanceView.as_view(), name='balance'),
]

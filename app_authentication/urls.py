# -*- coding: utf-8 -*-
from django.urls import path

# New report
from app_authentication.views import login, logout
from main.decorators import secure_required

urlpatterns = [
    path('login/', secure_required(login.LoginView.as_view()), name='login'),
    path('logout/', secure_required(logout.LogoutView.as_view()), name='logout'),
]

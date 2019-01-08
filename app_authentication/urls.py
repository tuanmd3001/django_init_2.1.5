# -*- coding: utf-8 -*-
from django.urls import path

# New report
from app_authentication.views import LoginView
from app_authentication.decorators import secure_required

urlpatterns = [
    path('login/', secure_required(LoginView.as_view()), name='login')
]

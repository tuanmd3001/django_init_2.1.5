# -*- coding: utf-8 -*-
from django.urls import path

# New report
from app_client import views

urlpatterns = [
    path('', views.home, name='app_home'),
]

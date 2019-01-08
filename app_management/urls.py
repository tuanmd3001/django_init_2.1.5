# -*- coding: utf-8 -*-
from django.urls import path

# New report
from app_management import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.home), name='config_dashboard')
]

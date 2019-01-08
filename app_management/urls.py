# -*- coding: utf-8 -*-
from django.urls import path

# New report
from app_management.views import dashboard

urlpatterns = [
    path('', dashboard.DashBoard.as_view(), name='config_dashboard')
]

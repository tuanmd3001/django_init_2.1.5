# -*- coding: utf-8 -*-
from django.urls import path, include

# New report
from app_management.views import dashboard, applications

urlpatterns = [
    path('system_config/', include([
        path('', dashboard.DashBoard.as_view(), name='config_dashboard'),
        path('reload/', applications.ReloadUrl.as_view(), name='config_reload_url'),
    ])),
]

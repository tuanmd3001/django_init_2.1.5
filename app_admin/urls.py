# -*- coding: utf-8 -*-
from django.urls import path, include

# New report
from app_admin.views import index

urlpatterns = [
    path('admin/', include([
        path('', index.Index.as_view(), name='admin_index'),
    ])),
]

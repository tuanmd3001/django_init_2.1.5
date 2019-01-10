# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.urls import path, include

urlpatterns = [
    path('users/', include([
        path('', lambda request: HttpResponse('Hello World!'), name='hello_world'),
    ])),
]
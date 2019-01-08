# -*- coding: utf-8 -*-
from django.db import models
# from main.models import *
from django.core.validators import RegexValidator


class AppUsers(models.Model):
    STATUS_SUSPENDED = 0
    STATUS_ACTIVATED = 1

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # birthday = models.DateField()
    # identification = models.CharField(max_length=12, unique=True,
    #                                   validators=[RegexValidator(r'^\d{,12}$', 'Số cmnd không hợp lệ')])
    # email = models.EmailField(max_length=75)
    # phone_number = models.CharField(max_length=30, validators=[
    #     RegexValidator(regex=r'^\d{6,15}$', message='Số điện thoại không đúng định dạng')])
    # status = models.BooleanField(default=STATUS_ACTIVATED)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

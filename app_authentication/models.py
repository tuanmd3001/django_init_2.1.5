# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel


class User(AbstractUser):
    STATUS_SUSPENDED = 0
    STATUS_ACTIVATED = 1

    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('user client access'),
        default=False,
        help_text=_('Designates whether the user can log into this client site.'),
    )
    is_admin = models.BooleanField(
        _('user client access'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    birthday = models.DateField()
    identification = models.CharField(max_length=12, unique=True,
                                      validators=[RegexValidator(r'^\d{,12}$', 'Số cmnd không hợp lệ')])
    phone_number = models.CharField(max_length=30, validators=[
        RegexValidator(regex=r'^\d{6,15}$', message='Số điện thoại không đúng định dạng')])
    status = models.BooleanField(default=STATUS_ACTIVATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

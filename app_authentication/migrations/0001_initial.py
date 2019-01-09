# Generated by Django 2.1.5 on 2019-01-08 13:26

import django.core.validators
from django.db import migrations, models
from datetime import datetime
from django.contrib.auth.admin import User
from app_authentication.models import AppUsers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    def create_superuser(apps, schema_editor):
        username = 'admin'
        password = 'admin'
        email = 'admin@teko.vn'
        now = datetime.now()

        superuser = User()
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.username = username
        superuser.email = email
        superuser.set_password(password)
        superuser.last_login = now.strftime("%Y-%m-%d %H:%M:%S")
        superuser.save()

        AppUsers.objects.create(
            id=1,
            username=username,
            email=email,
            birthday=now.strftime("%Y-%m-%d"),
        )

    operations = [
        migrations.CreateModel(
            name='AppUsers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('birthday', models.DateField()),
                ('identification', models.CharField(max_length=12, unique=True, validators=[
                    django.core.validators.RegexValidator('^\\d{,12}$', 'Số cmnd không hợp lệ')])),
                ('email', models.EmailField(max_length=75)),
                ('phone_number', models.CharField(max_length=30, validators=[
                    django.core.validators.RegexValidator(message='Số điện thoại không đúng định dạng',
                                                          regex='^\\d{6,15}$')])),
                ('status', models.BooleanField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'app_users',
            },
        ),
        migrations.RunPython(create_superuser),
    ]
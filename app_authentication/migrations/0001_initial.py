# Generated by Django 2.1.5 on 2019-01-09 10:11
from datetime import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
from app_authentication.models import User


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    def create_superuser(apps, schema_editor):
        username = 'admin'
        first_name = 'first'
        last_name = 'last'
        password = 'admin'
        email = 'admin@teko.vn'
        now = datetime.now()

        superuser = User()
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.username = username
        superuser.first_name = first_name
        superuser.last_name = last_name
        superuser.email = email
        superuser.set_password(password)
        superuser.birthday = now.strftime("%Y-%m-%d")
        superuser.save()

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this client site.', verbose_name='user client access')),
                ('is_admin', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='user admin access')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('birthday', models.DateField()),
                ('identification', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator('^\\d{,12}$', 'Số cmnd không hợp lệ')])),
                ('email', models.EmailField(max_length=75)),
                ('phone_number', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Số điện thoại không đúng định dạng', regex='^\\d{6,15}$')])),
                ('status', models.BooleanField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RunPython(create_superuser),
    ]

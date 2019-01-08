from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.cache import cache

from main.views import BaseView
from app_authentication.forms import LoginForm
from app_authentication.models import AppUsers
from app_authentication.routines import login_user
from django.contrib.auth import logout, REDIRECT_FIELD_NAME
from app_authentication.config import *

# Create your views here.
class LoginView(BaseView):
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        login_form = LoginForm()
        context['login_form'] = login_form
        context['redirect_field_name'] = REDIRECT_FIELD_NAME
        context['redirect_field_value'] = self.request.GET.get(REDIRECT_FIELD_NAME, 'app_home')
        return context

    def render_to_response(self, context, **response_kwargs):
        if not self.request.user or str(self.request.user) == 'AnonymousUser':
            if self.request.method == 'POST':
                login_form = LoginForm(self.request.POST)
                context['login_form'] = login_form
                if login_form.is_valid():
                    user = login_form.cleaned_data['user']
                    username = login_form.cleaned_data['username']
                    staff = AppUsers.objects.only('id').get(username=username)
                    staff_id = staff.id
                    self.request.session['staff_id'] = staff_id

                    url_next = self.request.POST.get(REDIRECT_FIELD_NAME, 'app_home')
                    if user.last_login == user.date_joined:
                        url_next = reverse('staff_change_password')

                    login_user(self.request, user)

                    cache.set(USER_SESSION_CACHE_KEY % staff_id, self.request.session.session_key, USER_SESSION_CACHE_TIME)

                    return redirect(url_next)
            return render(self.request, 'login.html', context)
        else:
            return redirect(reverse('app_home'))


class LogoutView(BaseView):
    def render_to_response(self, context, **response_kwargs):
        logout(self.request)
        return redirect(reverse('app_home'))
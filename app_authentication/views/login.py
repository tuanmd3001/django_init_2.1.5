from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.cache import cache
from django.urls import reverse

from app_authentication.config import *
from app_authentication.forms import LoginForm
from app_authentication.routines import login_user
from main.helpers.shortcuts import render, redirect
from main.views import BaseView


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
                    self.request.session['staff_id'] = user.id

                    url_next = self.request.POST.get(REDIRECT_FIELD_NAME, 'app_home')
                    if user.last_login == user.date_joined:
                        url_next = reverse('staff_change_password')

                    login_user(self.request, user)

                    cache.set(USER_SESSION_CACHE_KEY % user.id, self.request.session.session_key,
                              USER_SESSION_CACHE_TIME)

                    return redirect(url_next)
            return render(self.request, 'site/login.html', context)
        else:
            return redirect(reverse('app_home'))

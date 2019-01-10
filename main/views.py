import importlib.util
import inspect
import os

from constance import config
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.contrib.auth.views import redirect_to_login
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import resolve_url
from django.views.generic import TemplateView
from app_authentication.config import USER_SESSION_CACHE_KEY


class BaseView(TemplateView):
    def go_to_login(self):
        path = self.request.get_full_path()
        resolved_login_url = resolve_url('login' or settings.LOGIN_URL)
        return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)

    def validate_login_session(self):
        if self.request.user and str(self.request.user) != 'AnonymousUser':
            session_key = cache.get(USER_SESSION_CACHE_KEY % self.request.user.id, self.request.session.session_key)
            if session_key != self.request.session.session_key:
                logout(self.request)
                return False
        return True

    def dispatch(self, *args, **kwargs):
        dispatch = super(BaseView, self).dispatch(*args, **kwargs)
        if not settings.LOGIN_MULTI_LOCATION and not self.validate_login_session():
            return self.go_to_login()
        return dispatch

    def _handle_http_request(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self._handle_http_request(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._handle_http_request(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['settings'] = settings
        context['TEMPLATE_DIR'] = os.path.join(config.THEME, config.THEME_TEMPLATE_DIR)
        context['TEMPLATE_BASE_DIR'] = os.path.join(config.THEME, config.THEME_TEMPLATE_DIR, 'base.html')

        theme_configs = self.get_theme_configs()
        if theme_configs is not None:
            for name, obj in inspect.getmembers(theme_configs):
                if not inspect.isclass(obj) and not (name.startswith('__') or name.startswith('_')):
                    context[name] = obj
        return context

    def get_template_names(self):
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [os.path.join(config.THEME, config.THEME_TEMPLATE_DIR, self.template_name)]

    @staticmethod
    def get_theme_configs():
        try:
            spec = importlib.util.spec_from_file_location('theme_config.py',
                                                          os.path.join('app_themes', 'themes', config.THEME,
                                                                       'theme_config.py'))
            theme_configs = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(theme_configs)
            return theme_configs
        except:
            pass
        return None
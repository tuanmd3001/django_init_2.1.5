import inspect
import os
from constance import config
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView

from app_themes import theme_helpers


class BaseView(TemplateView):
    login_required = False
    admin_required = False
    superuser_required = False
    more_context = {}
    def dispatch(self, *args, **kwargs):
        dispatch = super(BaseView, self).dispatch(*args, **kwargs)
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
        context['TEMPLATE_DIR'] = theme_helpers.get_template_dir()
        context['TEMPLATE_BASE_DIR'] = theme_helpers.get_template_base_dir()
        if self.more_context:
            context.update(self.more_context)
            self.request.current_app = context.get('current_app', '')

        # theme_configs = theme_helpers.get_theme_configs()
        # if theme_configs is not None:
        #     for name, obj in inspect.getmembers(theme_configs):
        #         if not inspect.isclass(obj) and not (name.startswith('__') or name.startswith('_')):
        #             context[name] = obj
        return context

    def get_template_names(self):
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [os.path.join(config.THEME, config.THEME_TEMPLATE_DIR, self.template_name)]

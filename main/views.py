from django.views.generic import TemplateView
from django.conf import settings


class BaseView(TemplateView):
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
        return context
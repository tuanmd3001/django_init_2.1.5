from main.helpers.shortcuts import template_render

from app_admin.views.base import AdminBaseView


class Index(AdminBaseView):
    def render_to_response(self, context, **response_kwargs):
        return template_render(self.request, 'admin/index.html', context)

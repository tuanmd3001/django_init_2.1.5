from main.helpers.shortcuts import render

from app_admin.views.base import AdminBaseView


class Index(AdminBaseView):
    def render_to_response(self, context, **response_kwargs):
        return render(self.request, 'admin/index.html', context)

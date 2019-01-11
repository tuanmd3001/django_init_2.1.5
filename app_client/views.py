from django.shortcuts import render
from main.views import BaseView


class Index(BaseView):
    login_required = True
    def render_to_response(self, context, **response_kwargs):
        return render(self.request, 'app_client/index.html', context)

from django.shortcuts import render

from main.helpers.shortcuts import template_render
from main.views import BaseView

class Blank(BaseView):
    def render_to_response(self, context, **response_kwargs):
        return render(self.request, 'app_client/blankpage.html', context)
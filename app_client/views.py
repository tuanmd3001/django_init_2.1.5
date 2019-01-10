from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.template import loader

from main.views import BaseView


def home(request):
    template = loader.get_template('app_client/welcome.html')
    context = {}
    return HttpResponse(template.render(context, request))

class Blank(BaseView):
    def render_to_response(self, context, **response_kwargs):
        return render(self.request, 'app_client/blankpage.html', context)
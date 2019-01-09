from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

from main.views import BaseView


class LogoutView(BaseView):
    def render_to_response(self, context, **response_kwargs):
        logout(self.request)
        return redirect(reverse('app_home'))

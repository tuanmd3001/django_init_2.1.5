from django.shortcuts import render
from app_management.views.base import ManagementBaseView


class DashBoard(ManagementBaseView):
    def render_to_response(self, context, **response_kwargs):
        return render(self.request, 'dashboard.html', context)

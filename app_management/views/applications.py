from collections import OrderedDict
from importlib import import_module, reload
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps

from app_management.views.base import ManagementBaseView
import sys
from django.conf import settings


class ReloadUrl(ManagementBaseView):
    def render_to_response(self, context, **response_kwargs):
        self.reload_app()
        apps.get_app_config('app_admin')
        return render(self.request, 'app_management/dashboard.html', context)

    @staticmethod
    def reload_app():
        # To load the new app let's reset app_configs, the dictionary
        # with the configuration of loaded apps
        apps.app_configs = OrderedDict()
        # set ready to false so that populate will work
        apps.ready = False
        # re-initialize them all; is there a way to add just one without reloading them all?
        apps.populate(settings.INSTALLED_APPS)
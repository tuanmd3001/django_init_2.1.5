from django.utils.module_loading import autodiscover_modules

from app_client.sites import site, AppClientSite

__all__ = ["site", "AppClientSite"]

def autodiscover():
    autodiscover_modules('client', register_to=site)


default_app_config = 'app_client.apps.AppClientConfig'

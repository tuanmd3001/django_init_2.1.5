from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SimpleAppClientConfig(AppConfig):
    name = 'app_client'
    """Simple AppConfig which does not do automatic discovery."""

    default_site = 'app_client.AppClientSite'
    verbose_name = _("Application Client")

    # def ready(self):
        # checks.register(check_dependencies, checks.Tags.admin)
        # checks.register(check_admin_app, checks.Tags.admin)

class AppClientConfig(SimpleAppClientConfig):
    """The default AppConfig for client which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()


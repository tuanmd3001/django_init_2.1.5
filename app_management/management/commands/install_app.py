from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core import management


class Command(BaseCommand):
    help = 'List all app of project'

    def add_arguments(self, parser):
        parser.add_argument('app_name', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        apps = kwargs['app_name']
        for app in apps:
            self.stdout.write('>>> Checking app: ' + app)
            if app != '':
                if app not in settings.INSTALLED_APPS:
                    settings.INSTALLED_APPS.append(app)
                else:
                    self.stdout.write('>>> Application existed (' + app + ')!')

        management.call_command('apps_list')

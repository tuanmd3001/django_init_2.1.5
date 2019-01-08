from django.core.management.base import BaseCommand, CommandError
from django.conf import settings



class Command(BaseCommand):
    help = 'List all app of project'

    def handle(self, *args, **kwargs):
        self.stdout.write('>>> Installed apps:')
        self.stdout.write("\n".join([str(app) for app in settings.INSTALLED_APPS if not 'django' in app]))
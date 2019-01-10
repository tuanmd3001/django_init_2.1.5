from django.contrib import admin
from django.urls import path
import app_client
from django.apps import apps
from django.utils.translation import ugettext_lazy as _
from app_modules.users_manage.views import blank

class UsersManageClient(admin.ModelAdmin):
    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.module_name
        return [
            path('',
                self.admin_site.client_view(blank.Blank.as_view()),
                name='%s_%s_index' % info),
        ]

class Config(object):
    class Meta(object):
        app_label = 'users_manage'
        app_url_prefix = 'u'
        object_name = 'UsersManage'
        model_name = module_name = 'config'
        verbose_name_plural = _('config')
        abstract = False
        swapped = False

        @property
        def app_config(self):
            return apps.get_app_config(self.app_label)

        @property
        def label(self):
            return '%s.%s' % (self.app_label, self.object_name)

        @property
        def label_lower(self):
            return '%s.%s' % (self.app_label, self.model_name)

        @property
        def urls(self):
            return 'app_modules.users_manage.urls'

    _meta = Meta()

app_client.site.register([Config], UsersManageClient)
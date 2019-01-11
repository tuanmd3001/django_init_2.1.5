from django.apps import apps
from django.utils.translation import ugettext_lazy as _
import app_client
from app_client.options import ModelClient
from app_modules.users_manage.views import blank


class UsersManageClient(ModelClient):
    urlpatterns = [
        ('', blank.Blank.as_view(), 'users_index', 'Danh sách người dùng')
    ]


class Config(object):
    class Meta(object):
        app_label = 'users_manage'
        app_url_prefix = 'users'
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

    _meta = Meta()


app_client.site.register([Config], UsersManageClient)

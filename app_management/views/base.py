from main.views import BaseView
from django.utils.decorators import method_decorator

from app_authentication.decorators import superuser_required


class ManagementBaseView(BaseView):
    @method_decorator(superuser_required)
    def dispatch(self, *args, **kwargs):
        return super(ManagementBaseView, self).dispatch(*args, **kwargs)

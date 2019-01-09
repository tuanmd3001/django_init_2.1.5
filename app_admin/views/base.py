from django.utils.decorators import method_decorator

from main.views import BaseView

from django.contrib.auth.decorators import login_required


class AdminBaseView(BaseView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AdminBaseView, self).dispatch(*args, **kwargs)

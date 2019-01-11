from functools import update_wrapper

class ModelClient:
    urlpatterns = []
    url_desc = {}

    def __init__(self, model, client_site):
        self.model = model
        self.opts = model._meta
        self.client_site = client_site

    def __str__(self):
        return "%s.%s" % (self.model._meta.app_label, self.__class__.__name__)

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.client_site.client_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        url_patterns = []
        for pattern, view, name, description in self.urlpatterns:
            url_patterns.append(path(pattern, wrap(view), name=name))
            self.url_desc[name] = description
        return url_patterns

    @property
    def urls(self):
        return self.get_urls()

    @property
    def url_descriptions(self):
        return self.url_desc

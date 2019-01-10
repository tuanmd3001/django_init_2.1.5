class ModelClient:

    def __init__(self, model, client_site):
        self.model = model
        self.opts = model._meta
        self.client_site = client_site

    def __str__(self):
        return "%s.%s" % (self.model._meta.app_label, self.__class__.__name__)

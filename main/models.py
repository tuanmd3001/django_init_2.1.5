from django.db import models
from django.forms.models import model_to_dict

class BaseModel(models.Model):
    def dict(self, fields=None, exclude=None):
        return model_to_dict(self, fields, exclude)

    class Meta:
        abstract = True
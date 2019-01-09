from django.db import models
from django.forms.models import model_to_dict

from main.helpers.mysql_db_now.db_now import DBNow


class BaseModel(models.Model):
    def dict(self, fields=None, exclude=None):
        return model_to_dict(self, fields, exclude)

    class Meta:
        abstract = True


class BigAutoField(models.AutoField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] in ['django.db.backends.mysql', 'service_web.db_backends.mysql_db_now']:
            return "bigint AUTO_INCREMENT"
        else:
            return super(BigAutoField, self).db_type(connection)


class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] in ['django.db.backends.mysql', 'service_web.db_backends.mysql_db_now']:
            return "tinyint"
        else:
            return super(TinyIntegerField, self).db_type(connection)


class PositiveTinyIntegerField(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] in ['django.db.backends.mysql', 'service_web.db_backends.mysql_db_now']:
            return "tinyint unsigned"
        else:
            return super(PositiveTinyIntegerField, self).db_type(connection)


class AutoDBNowDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = DBNow()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(AutoDBNowDateTimeField, self).pre_save(model_instance, add)

    def get_prep_value(self, value):
        return value if isinstance(value, DBNow) else super(AutoDBNowDateTimeField, self).get_prep_value(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        return value if isinstance(value, DBNow) else super(AutoDBNowDateTimeField, self).get_db_prep_value(value,
                                                                                                            connection,
                                                                                                            prepared)

    def get_prep_lookup(self, lookup_type, value):
        return value if isinstance(value, DBNow) else super(AutoDBNowDateTimeField, self).get_prep_lookup(lookup_type,
                                                                                                          value)

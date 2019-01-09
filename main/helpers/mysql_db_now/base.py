from django.db.backends.mysql import base
from .db_now import DBNow


def adapt_db_now(value, conv):
    return str(value)


django_conversions = base.django_conversions.copy()
django_conversions.update({
    DBNow: adapt_db_now,
})


class DatabaseWrapper(base.DatabaseWrapper):
    def get_connection_params(self):
        kwargs = super(DatabaseWrapper, self).get_connection_params()
        kwargs['conv'] = django_conversions
        return kwargs

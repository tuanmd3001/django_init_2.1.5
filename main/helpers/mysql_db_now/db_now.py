class DBNow(object):
    def __str__(self):
        return 'NOW()'

    def as_sql(self, qn, val):
        return 'NOW()', {}

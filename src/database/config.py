import peewee


class BaseModelDB(peewee.Model):
    class Meta:
        peewee.order_by = id

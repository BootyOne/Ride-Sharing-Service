import peewee


class BaseModel(peewee.Model):
    class Meta:
        peewee.order_by = id

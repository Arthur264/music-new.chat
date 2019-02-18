from cassandra.cqlengine.models import Model


class BaseModel(Model):
    __abstract__ = True

    def to_dict(self):
        return {}

    @staticmethod
    def schema():
        return {}

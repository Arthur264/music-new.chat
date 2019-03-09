import abc
from cassandra.cqlengine.models import Model


class BaseModel(Model):
    __abstract__ = True

    @abc.abstractclassmethod
    def to_dict(self):
        return {}

    @staticmethod
    @abc.abstractclassmethod
    def schema():
        return {}

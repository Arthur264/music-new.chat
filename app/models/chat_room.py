import uuid
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class CharRoomModel(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(required=True)
    owner = columns.UUID(required=True)
    users = columns.Set(columns.UUID())
    create_at = columns.DateTime(default=datetime.now())

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'owner': self.owner,
            'users': self.users,
            'create_at': self.create_at,
        }

    @staticmethod
    def schema():
        return {
            'name': {'type': 'string', 'required': True},
            'users': {'type': 'set', 'required': False},
        }

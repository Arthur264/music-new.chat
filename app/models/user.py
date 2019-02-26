import uuid
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class UserModel(Model):
    id = columns.UUID(default=uuid.uuid4)
    first_name = columns.Text(required=True)
    last_name = columns.Text(required=True)
    username = columns.Text(required=True, primary_key=True)
    email = columns.Text(required=True)
    active = columns.Boolean(default=False)
    admin = columns.Boolean(default=False)
    create_at = columns.DateTime(default=datetime.now())

    def to_dict(self):
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'active': self.active,
            'admin': self.admin,
            'create_at': self.create_at,
        }

    @staticmethod
    def schema():
        return {
            'first_name': {
                'type': 'string',
                'required': True,
            },
            'last_name': {
                'type': 'string',
                'required': True,
            },
            'username': {
                'type': 'string',
                'required': True,
            },
            'password': {
                'type': 'string',
                'required': True,
                'min': 8,
            },
            'email': {
                'type': 'string',
                'required': True,
                'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            },
        }

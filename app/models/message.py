import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class MessageModel(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    chat_id = columns.UUID(required=True)
    user_id = columns.Integer(required=True)
    message = columns.Text(required=True)
    status = columns.Set(columns.Integer())
    create_at = columns.DateTime()

    def to_dict(self):
        return {
            'id': str(self.id),
            'chat_id': self.chat_id,
            'user_id': self.user_id,
            'message': self.message,
            'create_at': self.create_at,
        }

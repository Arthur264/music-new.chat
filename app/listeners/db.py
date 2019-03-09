from cassandra.cqlengine.management import sync_table

from app.models.chat_room import CharRoomModel
from app.models.message import MessageModel
from app.models.user import UserModel


def setup_db():
    sync_table(CharRoomModel)
    sync_table(MessageModel)
    sync_table(UserModel)

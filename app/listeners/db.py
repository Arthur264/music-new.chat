from cassandra.cqlengine.management import sync_table

from app.models.chat_room import CharRoomModel
from app.models.message import MessageModel


def setup_db():
    sync_table(CharRoomModel)
    sync_table(MessageModel)

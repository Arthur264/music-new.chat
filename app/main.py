import logging

from aiocassandra import aiosession
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from sanic import Sanic, Blueprint
from sanic_jwt import initialize

from app.app_logging import LOGGING
from app.models.chat_room import CharRoomModel
from app.models.message import MessageModel
from app.models.user import UserModel
from app.controllers.auth import authenticate
from app.views.room import RoomView
from app.views.user import UserView
from app.websockets import web_socket_chat
from config import PROJECT_ID, SANIC_SETTINGS

CLUSTER_KEY_SPACE = 'music_new_messages'
CLUSTER_NAME = 'music_new'
CLUSTER_HOST = '127.0.0.1'

cassandra_log = logging.getLogger()
cassandra_log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
cassandra_log.addHandler(handler)

SANIC_BLUEPRINT = Blueprint("blueprints", url_prefix="/blueprint", version=1)


def init_table():
    sync_table(CharRoomModel)
    sync_table(MessageModel)
    sync_table(UserModel)


def create_app(debug=True):
    log_config = LOGGING if not debug else None
    app = Sanic(PROJECT_ID, log_config=log_config)

    cluster = Cluster([CLUSTER_HOST])
    session = cluster.connect(keyspace=CLUSTER_KEY_SPACE)
    aiosession(session)
    # session.execute("DROP KEYSPACE " + CLUSTER_KEY_SPACE)

    connection.register_connection(CLUSTER_NAME, session=session)
    create_keyspace_simple(CLUSTER_KEY_SPACE, 1, connections=[CLUSTER_NAME])

    connection.setup([CLUSTER_HOST], CLUSTER_KEY_SPACE)

    init_table()

    app.debug = debug

    app.config.update(SANIC_SETTINGS)

    # Auth
    initialize(app, authenticate=authenticate)

    # Set routes
    app.add_route(RoomView.as_view(), '/room')
    app.add_route(UserView.as_view(), '/user')
    app.add_websocket_route(handler=web_socket_chat, uri="chat")

    app.blueprint(SANIC_BLUEPRINT)

    logging.info('Creating sanic app')
    return app

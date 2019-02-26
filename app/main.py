import logging

from sanic import Sanic, Blueprint
from sanic_jwt import initialize

from app.app_logging import LOGGING
from app.controllers.auth import authenticate
from app.views.room import RoomView
from app.views.user import UserView
from app.websockets import web_socket_chat
from config import PROJECT_ID, SANIC_SETTINGS, LOGGER_FORMAT

logger = logging.getLogger()
logger.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
logger.addHandler(handler)

SANIC_BLUEPRINT = Blueprint("blueprints", url_prefix="/blueprint", version=1)


def create_app(debug=True):
    log_config = LOGGING if not debug else None
    app = Sanic(PROJECT_ID, log_config=log_config)

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

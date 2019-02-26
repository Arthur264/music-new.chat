import logging

from sanic import Sanic, Blueprint
from sanic_jwt import initialize

from app.app_logging import LOGGING
from app.controllers.auth import authenticate
from app.listeners.events import before_server_start, after_server_stop
from app.views.room import RoomView
from app.views.user import UserView
from app.websockets import web_socket_chat
from config import PROJECT_ID, SANIC_SETTINGS

SANIC_BLUEPRINT = Blueprint("blueprints", url_prefix="/blueprint", version=1)


class MainSetup:
    _app = None

    @staticmethod
    def get_app():
        return MainSetup._app

    @staticmethod
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

        # Register listener
        app.register_listener(before_server_start, 'before_server_start')
        app.register_listener(after_server_stop, 'after_server_stop')

        app.blueprint(SANIC_BLUEPRINT)

        logging.info('Creating sanic app')
        MainSetup._app = app
        return app

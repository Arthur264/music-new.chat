from sanic_jwt.decorators import protected

from app.models.chat_room import CharRoomModel
from app.utils.validations import validate_json
from app.utils.view import ModelBaseView


class RoomView(ModelBaseView):
    model = CharRoomModel
    decorators = [
        validate_json(CharRoomModel.schema()),
        protected(),
    ]

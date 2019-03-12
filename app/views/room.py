from app.models.chat_room import CharRoomModel
from app.utils.validations import validate_json
from app.utils.view import ModelBaseView


class RoomView(ModelBaseView):
    model = CharRoomModel
    decorators = [
        validate_json(CharRoomModel.schema()),
    ]

    @staticmethod
    def prepare_data(request):
        user_id = request['user_id']
        result = request.json
        if CharRoomModel.objects(name=result['name']).len():
            pass

        result.update({
            'owner': user_id,
            'users': [user_id],
        })
        return result

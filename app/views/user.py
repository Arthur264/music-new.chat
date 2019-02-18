from app.models.user import UserModel
from app.utils.validations import validate_json
from app.utils.view import ModelBaseView


class UserView(ModelBaseView):
    model = UserModel
    decorators = [
        validate_json(UserModel.schema()),
    ]

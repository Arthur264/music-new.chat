from sanic_jwt import exceptions
from app.models.user import UserModel


async def authenticate(request, *args, **kwargs):
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        raise exceptions.AuthenticationFailed('Missing username or password.')

    user = UserModel.objects(username=username).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found.')

    if password != user.password:
        raise exceptions.AuthenticationFailed('Password is incorrect.')

    return user

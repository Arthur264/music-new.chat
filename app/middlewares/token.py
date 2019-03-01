from app.http import error_response
from app.utils.request import url_for


async def token_middleware(request):
    token = request.token
    if not token:
        return await error_response(msg='Token absent', status=401)

    print(token)
    status, data = await request.app.http(
        url_for('auth/user'),
        headers={'Authorization': f'Token {token}'},
        only_json=False,
    )
    if status == 401:
        return await error_response(msg='Token not valid', status=401)

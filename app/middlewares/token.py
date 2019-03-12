from app.http import error_response
from app.utils.request import url_for
from config import OPEN_PATHS


async def token_middleware(request):
    if any(request.path.startswith(path) for path in OPEN_PATHS):
        return

    token = request.token or request.raw_args.get('token')
    if not token:
        return await error_response(msg='Token absent', status=401)

    user_id = request.cookies.get('user_id')
    if user_id:
        request['user_id'] = user_id
        return

    status, user_data = await request.app.http(
        url_for('auth/user'),
        headers={'Authorization': f'Token {token}'},
        only_json=False,
    )
    if status == 401:
        return await error_response(msg='Token not valid', status=401)

    if status == 500:
        return await error_response(msg='Auth server return status 500.', status=500)

    request['user_id'] = str(user_data['id'])


async def cookie_middleware(request, response):
    if request.get('user_id'):
        response.cookies['user_id'] = request['user_id']

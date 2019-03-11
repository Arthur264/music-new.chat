from app.http import error_response
from app.utils.request import url_for
from config import OPEN_PATHS


async def token_middleware(request):
    if any(request.path.startswith(path) for path in OPEN_PATHS):
        return

    token = request.token or request.raw_args.get('token')
    if not token:
        return await error_response(msg='Token absent', status=401)

    status, data = await request.app.http(
        url_for('auth/user'),
        headers={'Authorization': f'Token {token}'},
        only_json=False,
    )
    if status == 401:
        return await error_response(msg='Token not valid', status=401)

    if status == 500:
        return await error_response(msg='Auth server return status 500.', status=500)

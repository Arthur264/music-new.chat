from app.http import error_response
from app.utils.request import url_for, fetch


async def token_middleware(request):
    token = request.token
    if not token:
        return error_response(msg='Token absent', status=401)

    status, data = await fetch(
        request.app.aiohttp_session,
        url_for('auth/user'),
        only_json=False,
    )
    if status == 401:
        return error_response(msg='Token not valid', status=401)

import uuid
from urllib.parse import urljoin

from sanic.request import Request
from sanic.response import json
from six import wraps

from app.http import error_response
from config import API_URL


def check_uuid(func):
    async def wrapper(*args, **kwargs):
        for arg in args:
            if not isinstance(arg, Request):
                continue

            try:
                param_id = arg.raw_args.get('id')
                if param_id:
                    uuid.UUID(param_id)
            except ValueError:
                return error_response(msg='Incorrect UUID.')

        return await func(*args, **kwargs)

    return wrapper


def authorized(methods=('PATCH', 'PUT', 'POST', 'DELETE')):
    def decorator(f):
        @wraps(f)
        async def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                response = await f(request, *args, **kwargs)
                return response

            if request.token:
                token = request.token
                user_id = await request.app.redis.get('TOKEN:{}'.format(token))
                if user_id:
                    response = await f(request, *args, **kwargs)
                    return response

            return json({}, 403)

        return wrapper

    return decorator


def url_for(url):
    return urljoin(API_URL, url)


async def fetch(session, url, only_json=True, **kwargs):
    async with session.get(url, **kwargs) as response:
        if only_json:
            return await response.json()
        else:
            return response.status, await response.json()

from sanic.response import json


async def json_response(data, status=None):
    response_status = status or 200
    return json(
        data,
        status=response_status,
    )


async def error_response(error_data=None, status=None, msg='Wrong request.'):
    response_status = status or 400
    response_data = error_data or {'error': msg}
    return json(
        response_data,
        status=response_status
    )

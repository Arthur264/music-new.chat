from functools import wraps

from cerberus import Validator
from sanic.request import Request
from sanic_validation.decorators import (
    _request_body_not_json_response,
    _validation_failed_response,
    JSON_DATA_ENTRY_TYPE,
)


def validate_json(schema, clean=False, methods=('PUT', 'POST')):
    validator = Validator(schema)

    def vd(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            request = next((arg for arg in args if isinstance(arg, Request)),
                           None)
            if not request:
                return ValueError('Args request not exist.')

            if request.method not in methods:
                response = await f(*args, **kwargs)
                return response

            if request.json is None:
                return _request_body_not_json_response()

            validation_passed = validator.validate(request.json or {})
            if validation_passed:
                if clean:
                    kwargs['valid_json'] = validator.document
                response = await f(*args, **kwargs)
                return response
            else:
                return _validation_failed_response(validator,
                                                   JSON_DATA_ENTRY_TYPE)

        return wrapper

    return vd

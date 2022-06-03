from functools import wraps
from typing import Literal, Type

import marshmallow
import werkzeug.exceptions
from flask import request

from main.engines import user as user_engine
from main.libs.jwt import get_jwt_data, get_jwt_token
from main.schemas.base import BaseSchema

from .exceptions import BadRequest, Unauthorized, ValidationError


def validate_request(http_element: Literal["params", "body"], schema: Type[BaseSchema]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                if http_element == "params":
                    kwargs["params"] = schema().load(request.args.to_dict())
                elif http_element == "body":
                    kwargs["data"] = schema().load(request.get_json())
                return f(*args, **kwargs)
            except werkzeug.exceptions.BadRequest as e:
                raise BadRequest(error_message=e.description)
            except marshmallow.ValidationError as e:
                raise ValidationError(error_data=e.messages)

        return wrapper

    return decorator


def require_not_existed_name(engine):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            name = kwargs["data"]["name"]
            if engine.find_by_name(name):
                raise BadRequest(error_message=f"{name} already existed")
            return f(*args, **kwargs)

        return wrapper

    return decorator


def require_authorized_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = get_jwt_token()
        data = get_jwt_data(token)
        user = user_engine.find_by_id(data["id"]) if data is not None else None

        if user:
            kwargs["user"] = user
            return f(*args, **kwargs)
        else:
            raise Unauthorized()

    return wrapper

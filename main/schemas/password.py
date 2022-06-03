from marshmallow import fields, validate

from .base import BaseSchema


class BasePasswordSchema(BaseSchema):
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{6,}$"),
    )

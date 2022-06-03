from marshmallow import fields

from .password import BasePasswordSchema


class AuthSchema(BasePasswordSchema):
    email = fields.Email(required=True, load_only=True)

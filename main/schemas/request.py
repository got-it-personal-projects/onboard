from marshmallow import fields, validate

from .base import BaseSchema


class PageParamSchema(BaseSchema):
    page = fields.Integer(required=True, validate=validate.Range(min=1))

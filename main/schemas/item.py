from marshmallow import fields, validate

from .base import BaseSchema, PaginationSchema


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(validate=validate.Length(min=0, max=1000))
    category_id = fields.Integer(dump_only=True)
    author_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ItemPaginationSchema(PaginationSchema):
    items = fields.List(fields.Nested(ItemSchema))

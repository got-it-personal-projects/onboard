from marshmallow import fields, validate

from .base import BaseSchema, PaginationSchema


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    author_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CategoryPaginationSchema(PaginationSchema):
    items = fields.List(fields.Nested(CategorySchema))

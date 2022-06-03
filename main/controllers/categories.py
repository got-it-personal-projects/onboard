from functools import wraps

from flask import jsonify

from main import app, config
from main.commons.decorators import (
    require_authorized_user,
    require_not_existed_name,
    validate_request,
)
from main.commons.exceptions import Forbidden, NotFound
from main.engines import category as category_engine
from main.schemas.category import CategoryPaginationSchema, CategorySchema
from main.schemas.request import PageParamSchema


def require_existed_category(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        category_id = kwargs["category_id"]
        category = category_engine.find_by_id(category_id)
        if category is None:
            raise NotFound(error_message=f"Category with id {category_id} not found")
        kwargs["category"] = category
        return f(*args, **kwargs)

    return wrapper


def require_category_author(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = kwargs["user"]
        category = kwargs["category"]
        if category.author != user:
            raise Forbidden()
        return f(*args, **kwargs)

    return wrapper


@app.route("/categories", methods=["GET"])
@validate_request("params", PageParamSchema)
def get_categories(params):
    page = params["page"]
    response = {
        "items_per_page": config.ITEMS_PER_PAGE,
        "page": page,
        "total_items": category_engine.get_categories_count(),
        "items": category_engine.get_categories(page, config.ITEMS_PER_PAGE),
    }
    return CategoryPaginationSchema().jsonify(response)


@app.route("/categories", methods=["POST"])
@validate_request("body", CategorySchema)
@require_not_existed_name(category_engine)
@require_authorized_user
def create_category(user, data):
    category = category_engine.create(author=user, **data)
    return CategorySchema().jsonify(category)


@app.route("/categories/<int:category_id>", methods=["DELETE"])
@require_existed_category
@require_authorized_user
@require_category_author
def delete_category(category, user, category_id):
    category_engine.delete(category)
    return jsonify({})

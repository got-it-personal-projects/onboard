from functools import wraps

from flask import jsonify

from main import app, config
from main.commons.decorators import (
    require_authorized_user,
    require_not_existed_name,
    validate_request,
)
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.controllers.categories import require_existed_category
from main.engines import item as item_engine
from main.schemas.item import ItemPaginationSchema, ItemSchema
from main.schemas.request import PageParamSchema


def require_existed_item(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        item_id = kwargs["item_id"]
        category = kwargs["category"]
        item = item_engine.find_by_id(item_id)
        if item is None:
            raise NotFound(error_message=f"Item with id {item_id} not found.")
        if item.category_id != category.id:
            raise BadRequest(
                error_message=f"Item with id {item_id} does not "
                f"belong to Category with id {category.id}"
            )
        kwargs["item"] = item
        return f(*args, **kwargs)

    return wrapper


def require_item_author(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        item = kwargs["item"]
        user = kwargs["user"]
        if item.author != user:
            raise Forbidden()
        return f(*args, **kwargs)

    return wrapper


@app.route("/categories/<int:category_id>/items", methods=["GET"])
@require_existed_category
@validate_request("params", PageParamSchema)
def get_items(category, params, category_id):
    page = params["page"]
    response = {
        "items_per_page": config.ITEMS_PER_PAGE,
        "page": page,
        "total_items": item_engine.get_items_count(category.id),
        "items": item_engine.get_items_in_category(
            category.id, page, config.ITEMS_PER_PAGE
        ),
    }
    return ItemPaginationSchema().jsonify(response)


@app.route("/categories/<int:category_id>/items", methods=["POST"])
@require_existed_category
@validate_request("body", ItemSchema)
@require_not_existed_name(item_engine)
@require_authorized_user
def create_item(user, category, data, category_id):
    item = item_engine.create(category=category, author=user, **data)
    return ItemSchema().jsonify(item)


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["GET"])
@require_existed_category
@require_existed_item
def get_item(item, category, category_id, item_id):
    return ItemSchema().jsonify(item)


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
@require_existed_category
@require_existed_item
@validate_request("body", ItemSchema)
@require_authorized_user
@require_item_author
def update_item(item, data, category, user, category_id, item_id):
    name = data["name"]
    existed_item = item_engine.find_by_name(name)
    if existed_item and existed_item.id != item.id:
        raise BadRequest(error_message=f"Item with name {name} already existed")
    item = item_engine.update(item=item, **data)
    return ItemSchema().jsonify(item)


@app.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
@require_existed_category
@require_existed_item
@require_authorized_user
@require_item_author
def delete_item(item, category, user, category_id, item_id):
    item_engine.delete(item)
    return jsonify({})

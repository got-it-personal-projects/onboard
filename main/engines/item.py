from typing import List, Optional

from sqlalchemy import func

from main import db
from main.models.category import CategoryModel
from main.models.item import ItemModel


def get_items_count(category_id: int) -> int:
    return ItemModel.query.filter(ItemModel.category_id == category_id).count()


def find_by_id(item_id: int) -> Optional[ItemModel]:
    return ItemModel.query.get(item_id)


def find_by_name(name: str) -> Optional[ItemModel]:
    return ItemModel.query.filter(
        func.lower(ItemModel.name) == func.lower(name)
    ).first()


def get_items_in_category(
    category_id: int, page: int, items_per_page: int
) -> List[ItemModel]:
    return (
        ItemModel.query.filter_by(category_id=category_id)
        .order_by(ItemModel.name)
        .paginate(page, items_per_page, False)
        .items
    )


def create(
    category: CategoryModel,
    author: str,
    name: str,
    description: Optional[str] = None,
) -> ItemModel:
    item = ItemModel(
        name=name, description=description, category=category, author=author
    )
    db.session.add(item)
    db.session.commit()
    return item


def update(item: ItemModel, name: str, description: Optional[str] = None) -> ItemModel:
    item.name = name
    item.description = description
    db.session.commit()
    return item


def delete(item: ItemModel) -> None:
    db.session.delete(item)
    db.session.commit()

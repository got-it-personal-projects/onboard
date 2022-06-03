from typing import List, Optional

from sqlalchemy import func

from main import db
from main.models.category import CategoryModel
from main.models.user import UserModel


def get_categories_count() -> int:
    return CategoryModel.query.count()


def find_by_name(name: str) -> Optional[CategoryModel]:
    return CategoryModel.query.filter(
        func.lower(CategoryModel.name) == func.lower(name)
    ).first()


def find_by_id(category_id: int) -> Optional[CategoryModel]:
    return CategoryModel.query.get(category_id)


def get_categories(page: int, items_per_page: int) -> List[CategoryModel]:
    return CategoryModel.query.paginate(page, items_per_page, False).items


def create(name: str, author: UserModel) -> CategoryModel:
    category = CategoryModel(name=name, author=author)
    db.session.add(category)
    db.session.commit()
    return category


def delete(category: CategoryModel) -> None:
    db.session.delete(category)
    db.session.commit()

from flask import Response

from main.engines import category as category_engine
from main.engines import item as item_engine
from main.engines import user as user_engine
from main.models.category import CategoryModel
from main.models.user import UserModel

valid_user_data = {
    "name": "Huy",
    "email": "vuhuy@gmail.com",
    "password": "Quanghuy0211",
}

valid_category_data = {"name": "Funny"}

valid_item_data = {"name": "Men fly"}

valid_jwt_token = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0"
    ".oJE2cjntukLvi0TeroOD1lNku1kjPE0_6RaeCiYsfug"
)


def create_user():
    return user_engine.create_user("vuhuy@gmail.com", "Huy", "Quanghuy0211")


def create_category(author: UserModel):
    return category_engine.create("Funny", author)


def create_item(category: CategoryModel, author: UserModel):
    return item_engine.create(category, author, "Men jump into water")


def generate_authorization_header(response: Response):
    return {"Authorization": f"Bearer {response.json['access_token']}"}

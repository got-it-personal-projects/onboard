from typing import Optional

import bcrypt

from main import db
from main.models.user import UserModel


def find_by_id(user_id: int) -> Optional[UserModel]:
    return UserModel.query.get(user_id)


def find_by_email(email: str) -> Optional[UserModel]:
    return UserModel.query.filter(UserModel.email == email).first()


def find_by_email_and_password(email: str, password: str) -> Optional[UserModel]:
    user = find_by_email(email)
    if not user or not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        return None
    return user


def create_user(email: str, name: str, password: str) -> UserModel:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = UserModel(name=name, email=email, hashed_password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

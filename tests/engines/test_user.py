import pytest

from main.engines import user as user_engine
from tests.helpers import create_user


def test_create_user_successfully():
    user = create_user()

    assert user is not None


def test_find_user_by_id_successfully():
    user = create_user()

    user = user_engine.find_by_id(user.id)

    assert user is not None


def test_find_not_found_user_by_id():
    user = user_engine.find_by_id(1)

    assert user is None


def test_find_user_by_email_successfully():
    user = create_user()

    user = user_engine.find_by_email(user.email)

    assert user is not None


def test_find_not_found_user_by_email():
    user = user_engine.find_by_email("vuhuy@gmail.com")

    assert user is None


def test_find_user_by_email_and_password_successfully():
    email = "vuhuy@gmail.com"
    name = "Huy"
    password = "123456"
    user_engine.create_user(email, name, password)

    user = user_engine.find_by_email_and_password(email, password)

    assert user is not None


@pytest.mark.parametrize(
    "email,password",
    [
        ("vuhuy1@gmail.com", "123456"),
        ("vuhuy@gmail.com", "1234567"),
    ],
)
def test_find_not_found_user_by_email_and_password(email, password):
    user_engine.create_user("vuhuy@gmail.com", "Huy", "123456")

    user = user_engine.find_by_email_and_password(email, password)

    assert user is None

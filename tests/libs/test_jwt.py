import pytest

from main.libs.jwt import create_access_token, get_jwt_data, verify_jwt_token
from main.models.user import UserModel
from tests.helpers import valid_jwt_token


def test_get_jwt_data_successfully():
    assert get_jwt_data(valid_jwt_token) is not None


def test_failed_to_get_jwt_data_with_invalid_jwt():
    assert get_jwt_data("invalid") is None


def test_verify_jwt_token_successfully():
    assert verify_jwt_token(valid_jwt_token) is True


def test_failed_to_verify_jwt_token_with_invalid_jwt():
    assert verify_jwt_token("invalid") is False


@pytest.mark.parametrize("identity", [1, "1", 1.0, {"1": 1}, [1], (1,), True])
def test_create_access_token_successfully(identity):
    access_token = create_access_token(identity)

    assert isinstance(access_token, str)
    assert verify_jwt_token(access_token) is True


@pytest.mark.xfail
@pytest.mark.parametrize(
    "invalid_identity",
    [
        UserModel(name="Huy", email="v@gmail.com", hashed_password="123456"),
        UserModel,
        {1},
        lambda x: x,
    ],
)
def test_failed_to_create_access_token_with_invalid_identity(invalid_identity):
    create_access_token(invalid_identity)

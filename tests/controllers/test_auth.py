import pytest

from tests.helpers import valid_user_data


def test_login_user_successfully(client):
    client.post("/users", json=valid_user_data)

    auth_response = client.post(
        "/auth",
        json={
            "email": valid_user_data["email"],
            "password": valid_user_data["password"],
        },
    )

    assert auth_response.status_code == 200
    assert "access_token" in auth_response.json


def test_login_user_with_invalid_email(client):
    client.post("/users", json=valid_user_data)

    response = client.post(
        "/auth",
        json={
            "email": f"invalid{valid_user_data['email']}",
            "password": valid_user_data["password"],
        },
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    "invalid_password",
    [
        "quanghuy",
        "QUANGHUY",
        "123456",
        "quanghuy0211",
        "QUANGHUY0211",
        "Quanghuy",
    ],
)
def test_login_user_with_invalid_password(client, invalid_password):
    client.post("/users", json=valid_user_data)

    response = client.post(
        "/auth", json={"email": valid_user_data["email"], "password": invalid_password}
    )

    assert response.status_code == 400

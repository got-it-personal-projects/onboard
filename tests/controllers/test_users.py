import pytest

from tests.helpers import generate_authorization_header, valid_user_data


class TestUserRegistration:
    def test_register_user_successfully(self, client):
        response = client.post(
            "/users",
            json=valid_user_data,
        )

        assert response.status_code == 200
        assert "access_token" in response.json

    def test_register_user_with_invalid_name(self, client):
        response = client.post(
            "/users",
            json={"name": "", "email": "vuhuy@gmail.com", "password": "Quanghuy0211"},
        )

        assert response.status_code == 400

    def test_register_user_with_invalid_email(self, client):
        response = client.post(
            "/users", json={"name": "Huy", "email": "vuhuy", "password": "Quanghuy0211"}
        )

        assert response.status_code == 400

    @pytest.mark.parametrize(
        "data",
        [
            {"name": "Huy", "email": "vuhuy@gmail.com", "password": "a"},
            {"name": "Huy", "email": "vuhuy@gmail.com", "password": "quanghuy"},
            {"name": "Huy", "email": "vuhuy@gmail.com", "password": "QUANGHUY"},
            {"name": "Huy", "email": "vuhuy@gmail.com", "password": "123456"},
            {"name": "Huy", "email": "vuhuy@gmail.com", "password": "quanghuy0211"},
            {"name": "Huy", "email": "vuhuy@gmail.com", "password": "QUANGHUY0211"},
            {"name": "Huy", "email": "vuhuy@gmail.com", "password": "Quanghuy"},
        ],
    )
    def test_register_user_with_invalid_password(self, client, data):
        response = client.post("/users", json=data)

        assert response.status_code == 400

    def test_register_user_with_existed_email(self, client):
        client.post(
            "/users",
            json=valid_user_data,
        )

        response = client.post(
            "/users",
            json=valid_user_data,
        )

        assert response.status_code == 400


class TestUserProfile:
    def test_get_user_profile_successfully(self, client):
        response = client.post("/users", json=valid_user_data)

        response = client.get(
            "/users/me",
            headers=generate_authorization_header(response),
        )

        assert response.status_code == 200

    def test_get_user_profile_by_unauthorized_user(self, client):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer invalid",
        }

        response = client.get("/users/me", headers=headers)

        assert response.status_code == 401

import math

import pytest

from main import config
from tests.helpers import (
    generate_authorization_header,
    valid_category_data,
    valid_user_data,
)


class TestCategoriesList:
    @pytest.mark.parametrize("pages_argument", [2.5, 2.4, 2, 1.5, 1.4, 1, 0.5, 0.4])
    def test_get_paginated_list_successfully(self, client, pages_argument):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        number_of_categories = int(config.ITEMS_PER_PAGE * pages_argument)
        for i in range(number_of_categories):
            client.post("/categories", json={"name": f"Category {i}"}, headers=headers)
        pages = math.ceil(pages_argument)

        for page in range(1, pages + 1):
            categories_response = client.get(f"/categories?page={page}")

            assert categories_response.status_code == 200
            if page < pages:
                assert len(categories_response.json["items"]) == config.ITEMS_PER_PAGE
            else:
                assert len(
                    categories_response.json["items"]
                ) == number_of_categories - (config.ITEMS_PER_PAGE * (pages - 1))

    def test_get_paginated_list_with_invalid_page_param(self, client):
        categories_response = client.get("/categories?page=0")

        assert categories_response.status_code == 400


class TestCategory:
    def test_create_category_successfully(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)

        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )

        assert category_response.status_code == 200

    def test_create_category_with_existed_name(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )

        category_response = client.post(
            "/categories",
            json={"name": category_response.json["name"]},
            headers=headers,
        )

        assert category_response.status_code == 400

    def test_create_category_with_invalid_name(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)

        category_response = client.post(
            "/categories", json={"name": ""}, headers=headers
        )

        assert category_response.status_code == 400

    def test_create_category_by_unauthorized_user(self, client):
        category_response = client.post(
            "/categories",
            json=valid_category_data,
            headers={"Authorization": "Bearer invalid"},
        )

        assert category_response.status_code == 401

    def test_delete_category_successfully(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )

        category_response = client.delete(
            f"/categories/{category_response.json['id']}", headers=headers
        )

        assert category_response.status_code == 200

    def test_delete_category_by_forbidden_user(self, client):
        user_response_1 = client.post(
            "/users",
            json={
                "email": "vuhuy@gmail.com",
                "name": "Huy",
                "password": "Quanghuy0211",
            },
        )
        headers_1 = generate_authorization_header(user_response_1)
        category_response_1 = client.post(
            "/categories", json=valid_category_data, headers=headers_1
        )
        user_response_2 = client.post(
            "/users",
            json={
                "email": "vuhuy1@gmail.com",
                "name": "Huy",
                "password": "Quanghuy0211",
            },
        )
        headers_2 = generate_authorization_header(user_response_2)

        category_response_2 = client.delete(
            f"/categories/{category_response_1.json['id']}", headers=headers_2
        )

        assert category_response_2.status_code == 403

    def test_delete_not_found_category(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)

        category_response = client.delete("/categories/100", headers=headers)

        assert category_response.status_code == 404

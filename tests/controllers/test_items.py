import math

import pytest

from main import config
from tests.helpers import (
    generate_authorization_header,
    valid_category_data,
    valid_item_data,
    valid_user_data,
)


class TestItemsList:
    @pytest.mark.parametrize("pages_argument", [2.5, 2.4, 2, 1.5, 1.4, 1, 0.5, 0.4])
    def test_get_paginated_list_successfully(self, client, pages_argument):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )
        number_of_items = int(config.ITEMS_PER_PAGE * pages_argument)
        for i in range(number_of_items):
            client.post(
                f"/categories/{category_response.json['id']}/items",
                json={"name": f"Item {i}"},
                headers=headers,
            )
        pages = math.ceil(pages_argument)

        for page in range(1, pages + 1):
            items_response = client.get(
                f"/categories/{category_response.json['id']}/items?page={page}"
            )

            assert items_response.status_code == 200
            if page < pages:
                assert len(items_response.json["items"]) == config.ITEMS_PER_PAGE
            else:
                assert len(items_response.json["items"]) == number_of_items - (
                    config.ITEMS_PER_PAGE * (pages - 1)
                )

    def test_get_paginated_list_with_invalid_page_param(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )

        items_response = client.get(
            f"/categories/{category_response.json['id']}/items?page=0"
        )

        assert items_response.status_code == 400


class TestItem:
    def test_create_item_successfully(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )

        item_response = client.post(
            f"/categories/{category_response.json['id']}/items",
            json=valid_item_data,
            headers=headers,
        )

        assert item_response.status_code == 200

    def test_create_item_with_invalid_name(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )

        item_response = client.post(
            f"/categories/{category_response.json['id']}/items",
            json={"name": ""},
            headers=headers,
        )

        assert item_response.status_code == 400

    def test_create_item_with_existed_name(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )
        category_id = category_response.json["id"]
        client.post(
            f"/categories/{category_id}/items",
            json=valid_item_data,
            headers=headers,
        )

        item_response = client.post(
            f"/categories/{category_id}/items",
            json=valid_item_data,
            headers=headers,
        )

        assert item_response.status_code == 400

    def test_get_item_successfully(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )
        category_id = category_response.json["id"]
        item_response = client.post(
            f"/categories/{category_id}/items",
            json=valid_item_data,
            headers=headers,
        )

        item_response = client.get(
            f"/categories/{category_id}/items/{item_response.json['id']}"
        )

        assert item_response.status_code == 200

    def test_get_not_found_item(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )

        item_response = client.get(
            f"/categories/{category_response.json['id']}/items/1"
        )

        assert item_response.status_code == 404

    def test_get_item_not_in_category(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response_1 = client.post(
            "/categories", json={"name": "Good"}, headers=headers
        )
        category_response_2 = client.post(
            "/categories", json={"name": "Funny"}, headers=headers
        )
        item_response = client.post(
            f"/categories/{category_response_1.json['id']}/items",
            json=valid_item_data,
            headers=headers,
        )

        item_response = client.get(
            f"/categories/{category_response_2.json['id']}"
            f"/items/{item_response.json['id']}"
        )

        assert item_response.status_code == 400

    def test_update_item_successfully(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )
        category_id = category_response.json["id"]
        item_response = client.post(
            f"/categories/{category_id}/items",
            json=valid_item_data,
            headers=headers,
        )

        item_response = client.put(
            f"/categories/{category_id}/items/{item_response.json['id']}",
            json={"name": "Men fly high"},
            headers=headers,
        )

        assert item_response.status_code == 200

    def test_update_item_with_existed_name_of_the_same_item(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )
        category_id = category_response.json["id"]
        item_response = client.post(
            f"/categories/{category_id}/items",
            json=valid_item_data,
            headers=headers,
        )

        item_response = client.put(
            f"/categories/{category_id}/items/{item_response.json['id']}",
            json=valid_item_data,
            headers=headers,
        )

        assert item_response.status_code == 200

    def test_update_item_with_existed_name_of_another_item(self, client):
        user_response = client.post("/users", json=valid_user_data)
        headers = generate_authorization_header(user_response)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers
        )
        category_id = category_response.json["id"]
        item_response = client.post(
            f"/categories/{category_id}/items",
            json={"name": "Movie"},
            headers=headers,
        )
        client.post(
            f"/categories/{category_id}/items",
            json={"name": "Play"},
            headers=headers,
        )

        item_response = client.put(
            f"/categories/{category_id}/items/{item_response.json['id']}",
            json={"name": "Play"},
            headers=headers,
        )

        assert item_response.status_code == 400

    def test_delete_item_by_forbidden_user(self, client):
        user_response_1 = client.post(
            "/users",
            json={
                "email": "vuhuy@gmail.com",
                "name": "Huy",
                "password": "Quanghuy0211",
            },
        )
        headers_1 = generate_authorization_header(user_response_1)
        category_response = client.post(
            "/categories", json=valid_category_data, headers=headers_1
        )
        category_id = category_response.json["id"]
        item_response = client.post(
            f"/categories/{category_id}/items",
            json=valid_item_data,
            headers=headers_1,
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

        item_response = client.delete(
            f"/categories/{category_id}/items/{item_response.json['id']}",
            headers=headers_2,
        )

        assert item_response.status_code == 403

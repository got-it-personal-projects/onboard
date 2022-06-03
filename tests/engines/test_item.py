import pytest

from main.engines import item as item_engine
from tests.helpers import create_category, create_item, create_user


def test_create_item_successfully():
    user = create_user()
    category = create_category(user)

    item = create_item(category, user)

    assert item is not None


def test_delete_item_successfully():
    user = create_user()
    category = create_category(user)
    item = create_item(category, user)

    assert item_engine.delete(item) is None


def test_get_items_count_successfully():
    user = create_user()
    category = create_category(user)

    count = item_engine.get_items_count(category.id)

    assert isinstance(count, int)
    assert count >= 0


def test_find_item_by_name_successfully():
    user = create_user()
    category = create_category(user)
    item = create_item(category, user)

    item = item_engine.find_by_name(item.name)

    assert item is not None


def test_find_not_found_item_by_name():
    item = item_engine.find_by_name("Funny")

    assert item is None


def test_find_item_by_id_successfully():
    user = create_user()
    category = create_category(user)
    item = create_item(category, user)

    category = item_engine.find_by_id(item.id)

    assert category is not None


def test_find_not_found_item_by_id():
    item = item_engine.find_by_id(1)

    assert item is None


def test_get_paginated_items_successfully():
    user = create_user()
    category = create_category(user)

    items = item_engine.get_items_in_category(category.id, 1, 20)

    assert isinstance(items, list)


@pytest.mark.parametrize("page,per_page", [(-1, 20), (1, -20), (-1, -20)])
def test_get_paginated_items_with_negative_pagination_values(page, per_page):
    user = create_user()
    category = create_category(user)

    items = item_engine.get_items_in_category(category.id, page, per_page)

    assert len(items) == 0

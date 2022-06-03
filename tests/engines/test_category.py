import pytest

from main.engines import category as category_engine
from tests.helpers import create_category, create_user


def test_create_category_successfully():
    user = create_user()

    category = create_category(user)

    assert category is not None


def test_delete_category_successfully():
    user = create_user()
    category = create_category(user)

    assert category_engine.delete(category) is None


def test_get_categories_count_successfully():
    count = category_engine.get_categories_count()

    assert isinstance(count, int)
    assert count >= 0


def test_find_category_by_name_successfully():
    user = create_user()
    category = create_category(user)

    category = category_engine.find_by_name(category.name)

    assert category is not None


def test_find_not_found_category_by_name():
    category = category_engine.find_by_name("Funny")

    assert category is None


def test_find_category_by_id_successfully():
    user = create_user()
    category = create_category(user)

    category = category_engine.find_by_id(category.id)

    assert category is not None


def test_find_not_found_category_by_id():
    category = category_engine.find_by_id(1)

    assert category is None


def test_get_paginated_categories_successfully():
    categories = category_engine.get_categories(1, 20)

    assert isinstance(categories, list)


@pytest.mark.parametrize("page,per_page", [(-1, 20), (1, -20), (-1, -20)])
def test_get_paginated_categories_with_negative_pagination_values(page, per_page):
    categories = category_engine.get_categories(page, per_page)

    assert len(categories) == 0

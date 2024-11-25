from http import HTTPStatus

import pytest

from products.models import Category


@pytest.mark.django_db
class TestCategoryAPI:

    category_url = '/api/categories/'
    category_detail_url = '/api/categories/{id}/'

    def check_category_fields(self, category_info, url):
        expected_fields = ('name', 'slug', 'image', 'subcategories')
        for field in expected_fields:
            assert field in category_info, (
                f'Ответ на GET-запрос к `{url}` '
                f'должен содержать поле `{field}`.'
            )

    def test_category_not_found(self, client):
        response = client.get(self.category_url)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.category_url}` не найден.'
        )

    def test_category_detail_not_found(self, client, category_1):
        response = client.get(
            self.category_detail_url.format(id=category_1.id)
        )
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.category_detail_url}` не найден.'
        )

    def test_category_not_auth(self, client):
        response = client.get(self.category_url)
        assert response.status_code == HTTPStatus.OK, (
            f'GET-запрос к `{self.category_url}` неавторизованного '
            'пользователя должен возвращать ответ со статусом 200.'
        )

    def test_category_detail_not_auth(self, client, category_1):
        response = client.get(
            self.category_detail_url.format(id=category_1.id)
        )
        assert response.status_code == HTTPStatus.OK, (
            f'GET-запрос к `{self.category_detail_url}` неавторизованного '
            'пользователя должен возвращать ответ со статусом 200.'
        )

    def test_category_auth_get(self, user_client, category_1):
        response = user_client.get(self.category_url)
        assert response.status_code == HTTPStatus.OK, (
            f'GET-запрос к `{self.category_url}` авторизованного '
            'пользователя должен возвращать ответ со статусом 200.'
        )
        test_data = response.json()
        assert isinstance(test_data, dict), (
            f'GET-запрос к `{self.category_url}` должен возвращать словарь.'
        )

        expected_fields = ('count', 'next', 'previous', 'results')
        for field in expected_fields:
            assert field in test_data, (
                f'Ответ на GET-запрос к `{self.category_url}` '
                f'должен содержать поле `{field}`.'
            )

        assert (
            len(test_data['results']) == Category.objects.count()
            or len(test_data['results']) == 5
        ), (
            f'GET-запрос к `{self.category_url}` должен возвращать'
            '5 первых категорий или все существующие, если их меньше 5.'
        )

        test_category = test_data['results'][0]
        self.check_category_fields(test_category, self.category_url)

    def test_category_detail_auth_get(self, user_client, category_1):
        response = user_client.get(
            self.category_detail_url.format(id=category_1.id)
        )
        assert response.status_code == HTTPStatus.OK, (
            f'GET-запрос к `{self.category_detail_url}` авторизованного '
            'пользователя должен возвращать ответ со статусом 200.'
        )
        test_data = response.json()

        assert isinstance(test_data, dict), (
            f'GET-запрос к `{self.category_detail_url}` '
            'должен возвращать словарь.'
        )

        self.check_category_fields(test_data, self.category_detail_url)

from http import HTTPStatus

import pytest


@pytest.mark.django_db
class TestShoppingCartAPI:

    shopping_cart_url = '/api/products/{id}/shopping_cart/'

    def test_shopping_cart_not_found(self, user_client, product_1):
        response = user_client.post(
            self.shopping_cart_url.format(id=product_1.id)
        )
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.shopping_cart_url}` не найден.'
        )

    def test_shopping_cart_not_auth(self, client, product_1):
        response = client.post(
            self.shopping_cart_url.format(id=product_1.id)
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'POST-запрос к `{self.shopping_cart_url}` неавторизованного '
            'пользователя должен возвращать ответ со статусом 401.'
        )

    def test_shopping_cart_auth(self, user_client, product_1):
        response = user_client.post(
            self.shopping_cart_url.format(id=product_1.id)
        )
        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос к `{self.shopping_cart_url}` авторизованного '
            'пользователя должен возвращать ответ со статусом 201.'
        )

        test_data = response.json()
        expected_fields = ('product', 'product_quantity', 'product_price')
        for field in expected_fields:
            assert field in test_data, (
                f'В ответе на POST-запрос к {self.shopping_cart_url} '
                f'должно содержаться поле {field}.'
            )

        test_product = test_data['product']
        expected_fields = (
            'name', 'slug', 'category', 'subcategory', 'price', 'images'
        )
        for field in expected_fields:
            assert field in test_product, (
                f'В ответе на POST-запрос к {self.shopping_cart_url} '
                f'поле `product` должно содержать {field}.'
            )

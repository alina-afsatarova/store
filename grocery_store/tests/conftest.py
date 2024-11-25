import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from products.models import Category, Product, Subcategory


@pytest.fixture
def category_1():
    return Category.objects.create(name='Категория 1', slug='category_1')


@pytest.fixture
def subcategory_1(category_1):
    return Subcategory.objects.create(
        name='Подкатегория 1', slug='subcategory_1', category=category_1
    )


@pytest.fixture
def product_1(category_1, subcategory_1):
    return Product.objects.create(
        name='Продукт 1',
        slug='product_1',
        price=100,
        category=category_1,
        subcategory=subcategory_1
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser',
        password='1234567',
    )


@pytest.fixture
def token_user(user):
    token = Token.objects.create(user=user)
    return {
        'auth_token': str(token),
    }


@pytest.fixture
def user_client(token_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_user["auth_token"]}')
    return client

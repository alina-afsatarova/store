from django.db.models import Sum
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import CartItem, Category, Product, ShoppingCart
from .serializers import (
    CartItemSerializer, CartItemQuantitySerializer, CategorySerializer,
    ProductSerializer, ShoppingCartSerializer,
)


@extend_schema(tags=['Category'])
@extend_schema_view(
    list=extend_schema(
        summary='Получение списка категорий.',
        description='Вывод списка категорий с подкатегориями с пагинацией.'
    ),
    retrieve=extend_schema(
        summary='Получение информации о конкретной категории.',
        description='Вывод категории с подкатегориями.'
    )
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny, )


@extend_schema(tags=['Product'])
@extend_schema_view(
    list=extend_schema(
        summary='Получение списка продуктов.',
        description='Вывод списка продуктов с пагинацией.',
    ),
    retrieve=extend_schema(
        summary='Получение информации о конкретном продукте.',
        description='Вывод информации о конкретном продукте.'
    ),
)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny, )

    def get_shopping_cart(self, request):
        shopping_cart, _ = ShoppingCart.objects.get_or_create(
            user=request.user
        )
        return shopping_cart

    def get_cart_item(self, request):
        return get_object_or_404(
            CartItem,
            shopping_cart=self.get_shopping_cart(request=request),
            product=self.get_object()
        )

    @extend_schema(
        tags=['Shopping Cart'],
        methods=["POST"],
        summary='Добавление продукта в корзину.',
        description="""Добавляет товар в корзину по id товара в url.
        При повторном POST-запросе с тем же id новая запись в БД не появится,
        а для существующей записи число товара `product_quantity`
        увеличивается на 1. В ответе на запрос выводится информация о товаре,
        суммарное количество этого товара и суммарная цена.
        """,
        request=None,
        responses={
            201: CartItemSerializer,
            401: None,
            404: None
        }
    )
    @extend_schema(
        tags=['Shopping Cart'],
        methods=['PATCH'],
        summary='Изменение количества продукта в корзине.',
        description='Изменение количества продукта в корзине.',
        request=CartItemQuantitySerializer,
        responses={
            200: CartItemSerializer,
            401: None,
            404: None
        }
    )
    @extend_schema(
        tags=['Shopping Cart'],
        methods=['DELETE'],
        summary='Удаление товара из корзины.',
        description='Удаление товара из корзины.',
        request=None,
        responses={
            204: None,
            401: None,
            404: None
        }
    )
    @action(
        detail=True,
        methods=['post', 'patch', 'delete'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, **kwargs):
        if request.method == 'POST':
            cart_item, _ = CartItem.objects.get_or_create(
                shopping_cart=self.get_shopping_cart(request=request),
                product=self.get_object()
            )
            cart_item.product_quantity += 1
            cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'PATCH':
            serializer = CartItemQuantitySerializer(
                self.get_cart_item(request=request),
                data=request.data,
                partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        self.get_cart_item(request=request).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Shopping Cart'])
class ShoppingCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_shopping_cart(self, request):
        shopping_cart, _ = ShoppingCart.objects.annotate(
            total_quantity=Sum('cart_items__product_quantity'),
            total_price=Sum('cart_items__product_price'),
        ).get_or_create(user=request.user)
        return shopping_cart

    @extend_schema(
        summary='Вывод состава корзины.',
        description=(
            'Вывод состава корзины с количеством товаров '
            'и суммарной стоимостью.'
        ),
        request=None,
        responses={
            200: ShoppingCartSerializer,
            401: None,
        }
    )
    def get(self, request):
        serializer = ShoppingCartSerializer(
            self.get_shopping_cart(request=request)
        )
        return Response(serializer.data)

    @extend_schema(
        summary='Полная очистка корзины.',
        description='Полная очистка корзины.',
        request=None,
        responses={
            204: None,
            401: None,
        }
    )
    def delete(self, request):
        cart_items = CartItem.objects.filter(
            shopping_cart=self.get_shopping_cart(request=request)
        )
        cart_items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

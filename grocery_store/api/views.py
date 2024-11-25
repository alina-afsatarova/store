from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import CartItem, Category, Product, ShoppingCart
from .serializers import (
    CartItemSerializer, CartItemQuantitySerializer, CategorySerializer,
    ProductSerializer, ShoppingCartSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny, )


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

    @action(
        detail=True,
        methods=['post', ],
        permission_classes=(permissions.IsAuthenticated,),

    )
    def shopping_cart(self, request, **kwargs):
        """Добавление товара в корзину."""
        cart_item, _ = CartItem.objects.get_or_create(
            shopping_cart=self.get_shopping_cart(request=request),
            product=self.get_object()
        )
        cart_item.product_quantity += 1
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_cart_item(self, request):
        return get_object_or_404(
            CartItem,
            shopping_cart=self.get_shopping_cart(request=request),
            product=self.get_object()
        )

    @shopping_cart.mapping.patch
    def patch_shopping_cart(self, request, **kwargs):
        """Изменение количества товара в корзине."""
        serializer = CartItemQuantitySerializer(
            self.get_cart_item(request=request),
            data=request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, **kwargs):
        """Удаление товара из корзины."""
        self.get_cart_item(request=request).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_shopping_cart(self, request):
        shopping_cart, _ = ShoppingCart.objects.annotate(
            total_quantity=Sum('cart_items__product_quantity'),
            total_price=Sum('cart_items__product_price'),
        ).get_or_create(user=request.user)
        return shopping_cart

    def get(self, request):
        """Вывод состава корзины с количеством товаров
        и суммарной стоимостью.
        """
        serializer = ShoppingCartSerializer(
            self.get_shopping_cart(request=request)
        )
        return Response(serializer.data)

    def delete(self, request):
        """Полная очистка корзины."""
        cart_items = CartItem.objects.filter(
            shopping_cart=self.get_shopping_cart(request=request)
        )
        cart_items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

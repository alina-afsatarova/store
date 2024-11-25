from rest_framework import serializers

from products.models import (
    CartItem, Category, Product, ProductImage, ShoppingCart, Subcategory
)


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = ('name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'slug', 'image', 'subcategories')

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        return serializer.data


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор модели Product."""

    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'slug', 'category', 'subcategory', 'price', 'images')

    def get_images(self, obj):
        images = obj.product_images
        serializer = ProductImageSerializer(images, many=True)
        return serializer.data


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор модели CartItem."""

    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('product', 'product_quantity', 'product_price')


class CartItemQuantitySerializer(serializers.ModelSerializer):
    """Сериализатор при PATCH-запросах на изменение количества
    продукта в корзине.
    """

    class Meta:
        model = CartItem
        fields = ('product_quantity', )

    def validate(self, data):
        if not data.get('product_quantity'):
            raise serializers.ValidationError('Укажите количество продукта!')
        return data

    def to_representation(self, instance):
        serializer = CartItemSerializer(instance)
        return serializer.data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор модели ShoppingCart."""

    products = serializers.SerializerMethodField()
    total_quantity = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('products', 'total_quantity', 'total_price')

    def get_products(self, obj):
        cart_items = obj.cart_items.all()
        serializer = CartItemSerializer(cart_items, many=True)
        return serializer.data

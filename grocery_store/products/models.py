from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Категория продукта."""
    name = models.CharField('Наименование', max_length=128, blank=False)
    slug = models.SlugField(max_length=32, unique=True, blank=False)
    image = models.ImageField(
        'Изображение',
        upload_to='categories/',
        blank=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Подкатегория продукта."""
    name = models.CharField('Наименование', max_length=128, blank=False)
    slug = models.SlugField(max_length=32, unique=True, blank=False)
    image = models.ImageField(
        'Изображение',
        upload_to='subcategories/',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Продукт."""
    name = models.CharField('Наименование', max_length=128, blank=False)
    slug = models.SlugField(max_length=32, unique=True, blank=False)
    price = models.FloatField('Цена', validators=(MinValueValidator(1),))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегория'
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images',
        verbose_name='Продукт'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='products/'
    )

    class Meta:
        verbose_name = 'изображение продукта'
        verbose_name_plural = 'Изображения продукта'

    def __str__(self):
        return f'Изображение продукта {self.product.name}'


class ShoppingCart(models.Model):
    """Корзина."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина пользователя - {self.user.username}'


class CartItem(models.Model):
    """Продукт в корзине."""
    shopping_cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    product_quantity = models.PositiveSmallIntegerField(
        'Количество продукта',
        null=True,
        default=0,
        validators=(MinValueValidator(1),)
    )
    product_price = models.FloatField('Цена продуктов', default=0)

    def save(self, *args, **kwargs):
        self.product_price = self.product_quantity * self.product.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'продукт в корзине'
        verbose_name_plural = 'Продукты в корзинах'

    def __str__(self):
        return f'Продукт в корзине {self.shopping_cart.user.username}'

from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField("Session Key", max_length=100, null=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        if self.user:
            return f"Корзина пользователя {self.user.username}"
        return f"Корзина (сессия: {self.session_key})"

    def get_total_price(self):
        """Общая стоимость товаров в корзине"""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_total_items(self):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('goods.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_subtotal(self):
        """Стоимость позиции"""
        return self.product.price * self.quantity

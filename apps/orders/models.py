from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    """Заказ покупателя"""
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('processing', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    phone = models.CharField("Телефон", max_length=20)
    address = models.TextField("Адрес доставки")
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.created_at.strftime('%d.%m.%Y')}"

    def get_total_price(self):
        """Общая стоимость заказа"""
        return sum(item.get_subtotal() for item in self.items.all())


class OrderItem(models.Model):
    """Элемент заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('goods.Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField("Количество", default=1)
    price = models.DecimalField("Цена (₽)", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"{self.product.name if self.product else 'Удаленный товар'} x {self.quantity}"

    def get_subtotal(self):
        """Стоимость позиции"""
        return self.price * self.quantity

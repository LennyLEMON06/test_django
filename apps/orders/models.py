from django.db import models
from django.conf import settings


class Order(models.Model):
    """Заказ (заявка)"""
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('processing', 'В обработке'),
        ('confirmed', 'Подтверждён'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Пользователь")
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100, blank=True)
    phone = models.CharField("Телефон", max_length=20)
    address = models.CharField("Адрес доставки", max_length=255, blank=True)
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    total_price = models.DecimalField("Общая сумма", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ №{self.id} от {self.first_name}"

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """Элемент заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('goods.Product', on_delete=models.SET_NULL, null=True, related_name='order_items')
    product_name = models.CharField("Название товара", max_length=200, default='', blank=True)  # Копия названия на момент заказа
    quantity = models.PositiveIntegerField("Количество", default=1)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField("Сумма", max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

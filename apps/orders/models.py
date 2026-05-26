from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    """Заказ (заявка)"""
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('processing', 'В обработке'),
        ('confirmed', 'Подтверждён'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        verbose_name='Пользователь'
    )
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес доставки')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Заказ №{self.id} - {self.first_name} {self.last_name}'
    
    def get_total_price(self):
        return sum(item.get_total() for item in self.items.all())


class OrderItem(models.Model):
    """Элемент заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey('goods.Product', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена на момент заказа')
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказов'
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
    
    def get_total(self):
        return self.price * self.quantity

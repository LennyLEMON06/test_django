from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        verbose_name='Пользователь'
    )
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name='Сессия')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username}'
        return f'Корзина (сессия: {self.session_key})'
    
    def get_total_price(self):
        return sum(item.get_total() for item in self.items.all())


class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product = models.ForeignKey('goods.Product', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
    
    def get_total(self):
        return self.product.price * self.quantity

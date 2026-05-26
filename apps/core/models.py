from django.db import models


class ContactInfo(models.Model):
    """Контактная информация магазина"""
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    address = models.TextField(verbose_name='Адрес')
    
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
    
    def __str__(self):
        return f'{self.phone} - {self.address}'


class Slider(models.Model):
    """Слайдер для главной страницы"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='Подзаголовок')
    image = models.ImageField(upload_to='slider/', verbose_name='Изображение')
    link = models.URLField(blank=True, null=True, verbose_name='Ссылка')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    
    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайдер'
        ordering = ['order']
    
    def __str__(self):
        return self.title

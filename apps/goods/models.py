from django.db import models


class Category(models.Model):
    """Категория товаров/услуг"""
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар или услуга"""
    PRODUCT_TYPE_CHOICES = [
        ('product', 'Товар'),
        ('service', 'Услуга'),
    ]
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    product_type = models.CharField(
        max_length=10, 
        choices=PRODUCT_TYPE_CHOICES, 
        default='product',
        verbose_name='Тип'
    )
    is_popular = models.BooleanField(default=False, verbose_name='Популярный')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    # Характеристики для памятников
    monument_length = models.PositiveIntegerField(blank=True, null=True, verbose_name='Длина (см)')
    monument_width = models.PositiveIntegerField(blank=True, null=True, verbose_name='Ширина (см)')
    monument_thickness = models.PositiveIntegerField(blank=True, null=True, verbose_name='Толщина (см)')
    monument_material = models.CharField(max_length=100, blank=True, verbose_name='Материал')
    
    # Характеристики для плитки
    tile_length = models.PositiveIntegerField(blank=True, null=True, verbose_name='Длина плитки (см)')
    tile_width = models.PositiveIntegerField(blank=True, null=True, verbose_name='Ширина плитки (см)')
    tile_coating = models.CharField(max_length=100, blank=True, verbose_name='Тип покрытия')
    tile_package_quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name='В упаковке (шт)')
    
    class Meta:
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары и услуги'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} - {self.price} ₽'

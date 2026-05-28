from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Категория товаров/услуг"""
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField("URL", unique=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Товар или услуга"""
    PRODUCT_TYPE_CHOICES = [
        ('product', 'Товар'),
        ('service', 'Услуга'),
    ]

    MATERIAL_CHOICES = [
        ('granite', 'Гранит'),
        ('marble', 'Мрамор'),
        ('limestone', 'Известняк'),
        ('composite', 'Композит'),
        ('metal', 'Металл'),
        ('other', 'Другое'),
    ]

    FENCE_MATERIAL_CHOICES = [
        ('metal_profile', 'Металлический профиль'),
        ('steel_pipe', 'Стальная труба'),
        ('wrought_iron', 'Кованое железо'),
        ('aluminum', 'Алюминий'),
        ('chain_link', 'Сетка рабица'),
        ('other', 'Другое'),
    ]

    COATING_CHOICES = [
        ('polished', 'Полированная'),
        ('matte', 'Матовая'),
        ('brushed', 'Брашированная'),
        ('thermal', 'Термообработанная'),
        ('natural', 'Натуральная'),
    ]

    # Основные поля
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField("URL", unique=True, blank=True)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена (₽)", max_digits=10, decimal_places=2)
    image = models.ImageField("Изображение", upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    product_type = models.CharField("Тип", max_length=10, choices=PRODUCT_TYPE_CHOICES, default='product')
    is_popular = models.BooleanField("Популярный", default=False)

    # Поля для памятников
    length_p = models.DecimalField("Длина (см)", max_digits=6, decimal_places=1, blank=True, null=True)
    width_p = models.DecimalField("Ширина (см)", max_digits=6, decimal_places=1, blank=True, null=True)
    thickness_p = models.DecimalField("Толщина (см)", max_digits=6, decimal_places=1, blank=True, null=True)
    material = models.CharField("Материал", max_length=20, choices=MATERIAL_CHOICES, blank=True, default='')

    # Поля для плитки
    tile_length = models.DecimalField("Длина плитки (см)", max_digits=6, decimal_places=1, blank=True, null=True)
    tile_width = models.DecimalField("Ширина плитки (см)", max_digits=6, decimal_places=1, blank=True, null=True)
    tile_thickness = models.DecimalField("Толщина (мм)", max_digits=4, decimal_places=1, blank=True, null=True)
    coating_type = models.CharField("Тип покрытия", max_length=30, choices=COATING_CHOICES, blank=True, default='')
    quantity_per_pack = models.PositiveIntegerField("Количество в упаковке (шт)", blank=True, null=True)

    # Поля для услуг
    service_duration = models.PositiveIntegerField("Срок выполнения (дни)", blank=True, null=True)
    service_notes = models.TextField("Особенности услуги", blank=True, default='')

    # Поля для оградки
    fence_height = models.DecimalField("Высота оградки (см)", max_digits=6, decimal_places=1, blank=True, null=True)
    fence_pattern_height = models.DecimalField("Высота рисунка (см)", max_digits=6, decimal_places=1, blank=True, null=True)
    fence_material = models.CharField("Материал оградки", max_length=30, choices=FENCE_MATERIAL_CHOICES, blank=True, default='')

    created_at = models.DateTimeField("Дата создания", auto_now_add=True, null=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True, null=True)

    class Meta:
        verbose_name = "Товар/Услуга"
        verbose_name_plural = "Товары и услуги"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

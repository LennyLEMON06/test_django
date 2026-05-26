from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Категория товаров/услуг"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("URL", unique=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар или услуга"""
    TYPE_CHOICES = [
        ('product', 'Товар'),
        ('service', 'Услуга'),
    ]

    MATERIAL_CHOICES = [
        ('granite', 'Гранит'),
        ('marble', 'Мрамор'),
        ('gabbro', 'Габбро'),
        ('other', 'Другое'),
    ]

    COATING_CHOICES = [
        ('polished', 'Полированная'),
        ('matt', 'Матовая'),
        ('thermo', 'Термообработка'),
        ('bush', 'Бучардированная'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Изображение", upload_to='products/', blank=True, null=True)
    product_type = models.CharField("Тип", max_length=10, choices=TYPE_CHOICES, default='product')
    is_popular = models.BooleanField("Популярный", default=False)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    # Характеристики для памятников
    monument_length = models.PositiveIntegerField("Длина (см)", blank=True, null=True, help_text="Для памятников")
    monument_width = models.PositiveIntegerField("Ширина (см)", blank=True, null=True, help_text="Для памятников")
    monument_thickness = models.PositiveIntegerField("Толщина (см)", blank=True, null=True, help_text="Для памятников")
    material = models.CharField("Материал", max_length=20, choices=MATERIAL_CHOICES, blank=True, null=True)

    # Характеристики для плитки
    tile_length = models.PositiveIntegerField("Длина плитки (см)", blank=True, null=True, help_text="Для плитки")
    tile_width = models.PositiveIntegerField("Ширина плитки (см)", blank=True, null=True, help_text="Для плитки")
    coating_type = models.CharField("Тип покрытия", max_length=20, choices=COATING_CHOICES, blank=True, null=True)
    tiles_per_pack = models.PositiveIntegerField("Штук в упаковке", blank=True, null=True, help_text="Для плитки")

    class Meta:
        verbose_name = "Товар/Услуга"
        verbose_name_plural = "Товары и услуги"
        ordering = ['-is_popular', 'name']

    def __str__(self):
        return self.name

    def get_total_price(self):
        return self.price

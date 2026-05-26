from django.db import models


class ContactInfo(models.Model):
    """Контактная информация магазина"""
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    address = models.CharField("Адрес", max_length=255)
    working_hours = models.CharField("Режим работы", max_length=255, blank=True)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.phone


class Slider(models.Model):
    """Слайдер для главной страницы"""
    title = models.CharField("Заголовок", max_length=100)
    subtitle = models.CharField("Подзаголовок", max_length=255, blank=True, default='')
    image = models.ImageField("Изображение", upload_to='slider/')
    link = models.URLField("Ссылка", blank=True, default='')
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайдер"
        ordering = ['order']

    def __str__(self):
        return self.title

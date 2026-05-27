from django.db import models


class ContactInfo(models.Model):
    """Контактная информация магазина"""
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    address = models.TextField("Адрес")
    work_hours = models.TextField("Режим работы")
    is_active = models.BooleanField("Активно", default=True)

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def __str__(self):
        return f"{self.phone} - {self.email}"


class Slider(models.Model):
    """Слайдер для главной страницы"""
    title = models.CharField("Заголовок", max_length=255, blank=True)
    image = models.ImageField("Изображение", upload_to='slider/')
    order = models.IntegerField("Порядок отображения", default=0)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайдер"
        ordering = ['order']

    def __str__(self):
        return self.title or f"Слайд #{self.id}"


class ContactRequest(models.Model):
    """Обращения с сайта через форму обратной связи"""
    name = models.CharField("Ваше имя", max_length=255)
    email = models.EmailField("Email")
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_processed = models.BooleanField("Обработано", default=False)

    class Meta:
        verbose_name = "Обращение с сайта"
        verbose_name_plural = "Обращения с сайта"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d.%m.%Y')}"

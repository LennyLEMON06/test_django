from django.db import models


class News(models.Model):
    """Новость магазина"""
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст")
    image = models.ImageField("Изображение", upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_short_text(self):
        return self.text[:150] + '...' if len(self.text) > 150 else self.text

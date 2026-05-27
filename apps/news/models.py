from django.db import models


class News(models.Model):
    """Новость магазина"""
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Текст новости")
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    image = models.ImageField("Изображение", upload_to='news/', blank=True, null=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_short_content(self, length=100):
        """Краткое содержание новости"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + '...'

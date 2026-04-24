from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class MyBlog(models.Model):
    name = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL")
    description = models.TextField(verbose_name="Содержание")
    preview = models.ImageField(upload_to="blog/previews/", blank=True, null=True, verbose_name="Превью")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    # Добавим поле для отслеживания, отправляли ли уже поздравление
    congratulation_sent = models.BooleanField(default=False, verbose_name="Поздравление отправлено")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Записи блога"
        ordering = ['-created_at']
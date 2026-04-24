from django.db import models
from django.urls import reverse

class MyBlog(models.Model):
    name = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Содержание")
    preview = models.ImageField(upload_to="blog/previews/", blank=True, null=True, verbose_name="Превью")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Записи блога"
        ordering = ['-created_at']
from django.db import models


class TimeStampedModel(models.Model):
    """Абстрактная модель с полями времени"""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        abstract = True


class Category(TimeStampedModel):  # ✅ Теперь у категории тоже есть время
    name = models.CharField(max_length=50, verbose_name="Наименование")
    description = models.CharField(max_length=100, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name="Наименование")
    description = models.CharField(max_length=100, verbose_name="Описание")
    image = models.ImageField(upload_to="product/photo", blank=True, null=True, verbose_name="Изображение")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

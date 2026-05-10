from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Кастомная модель пользователя с email в качестве логина"""

    # Убираем username, делаем email обязательным
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # Дополнительные поля
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Номер телефона'
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Страна'
    )

    # Используем email для авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Поля, обязательные при создании суперпользователя

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

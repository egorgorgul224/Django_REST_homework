from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Модель пользователь. Содержит поля email, city, phone, avatar."""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    city = models.CharField(max_length=100, verbose_name="Страна", blank=True, null=True)
    phone = models.CharField(max_length=35, verbose_name="Телефон", blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", verbose_name="Аватар", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}, {self.is_active}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]

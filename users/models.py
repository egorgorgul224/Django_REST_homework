from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course


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


class Payment(models.Model):
    """Модель платеж(оплата). Содержит поля user(модель User), course(модель Course), method(способ оплаты: наличные
    или перевод на счет), session_id, link."""

    Cash = "cash"
    Transfer = "transfer"

    STATUS_CHOICES = [
        (Cash, "Наличные"),
        (Transfer, "Перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments", verbose_name="Платеж")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="payments")
    method = models.CharField(choices=STATUS_CHOICES, default=Transfer, verbose_name="Способ оплаты")
    session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID сессии", help_text="Укажите ID сессии"
    )
    link = models.URLField(
        max_length=400, blank=True, null=True, verbose_name="Ссылка на оплату", help_text="Укажите ссылку на оплату"
    )

    def __str__(self):
        return f"{self.user}: {self.method} - {self.course} - {self.course.get("amount")}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-id"]


class Subscription(models.Model):
    """Модель подписка. Содержит поля created_at, user, course."""

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscriptions")

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["id"]

from django.contrib import admin

from users.models import User


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    """Админ панель с пользователями. Поля для отображения: id, email."""

    list_display = (
        "id",
        "email",
    )

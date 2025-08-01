from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация модели User. Предоставлен доступ к редактированию полей: first_name, last_name, city, phone,
    avatar."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "city", "phone", "avatar"]

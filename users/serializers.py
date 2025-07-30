from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация модели User. Используются все поля."""

    class Meta:
        model = User
        fields = "__all__"

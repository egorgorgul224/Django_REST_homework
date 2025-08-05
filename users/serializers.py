from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализация модели Payment. Предоставлен доступ ко всем полям."""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Сериализация модели User. Предоставлен доступ к редактированию полей: first_name, last_name, city, phone,
    avatar."""

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "city", "payments"]


class RegisterUserSerializer(serializers.ModelSerializer):
    """Сериализация модели User для регистрации/создания пользователя. Предоставлен доступ к полям: email, password,
    payments."""

    class Meta:
        model = User
        fields = ["email", "password", "payments"]

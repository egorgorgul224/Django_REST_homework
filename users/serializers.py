from rest_framework import serializers

from users.models import Payment, Subscription, User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализация модели Payment. Предоставлен доступ ко всем полям."""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Сериализация модели User. Предоставлен доступ доступ к полям: first_name, last_name, city, phone, avatar."""

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "city", "payments"]


class UserMinInfoSerializer(serializers.ModelSerializer):
    """Сериализация модели User для просмотра минимальной информации о пользователе, если пользователь не является
    владельцем аккаунта. Предоставлен доступ к полям: email, first_name, city, date_joined."""

    class Meta:
        model = User
        fields = ["email", "first_name", "city", "date_joined"]


class RegisterUserSerializer(serializers.ModelSerializer):
    """Сериализация модели User для регистрации/создания пользователя. Предоставлен доступ к полям: email, password,
    payments."""

    class Meta:
        model = User
        fields = ["email", "password", "payments"]


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализация модели Subscription. Предоставлен доступ ко всем полям, кроме 'created_at'."""

    class Meta:
        model = Subscription
        exclude = ["created_at"]

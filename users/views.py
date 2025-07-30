from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Класс ViewSet модели User для создания и удаления пользователя, вывода списка пользователей и информации о
    каждом пользователи."""

    serializer_class = UserSerializer
    queryset = User.objects.all()

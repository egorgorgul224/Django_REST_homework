from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        """Функция проверяет, является пользователь модератором или нет. Если модератор - возвращает True, иначе
        False."""

        return request.user.groups.filter(name="moderator").exists()

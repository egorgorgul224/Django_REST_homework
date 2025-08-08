from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Класс проверяет, является пользователь модератором или нет. Если модератор - возвращает True, иначе False."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(BasePermission):
    """Класс проверяет, что пользователь является владельцем курса или урока. Если владелец - возвращает True, иначе
    False."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsOwnerAccount(BasePermission):
    """Класс проверяет, что пользователь является владельцем аккаунта. Если владелец - возвращает True, иначе False."""

    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        return False

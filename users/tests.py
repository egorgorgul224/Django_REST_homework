from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User


class SubscriptionTestCase(APITestCase):
    """Класс описывает тесты для модели Subscription."""

    def setUp(self):
        """Метод для создания первичных данных: пользователь, курс, токен авторизации."""

        self.user = User.objects.create(email="admin@mail.ru")
        self.course = Course.objects.create(name="Test Course", amount=1000, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_subscription(self):
        """Тест проверяет работу контроллера SubscriptionAPIView добавления/удаления подписки на курс. Проверяется
        корректный возврат статуса 200 и сообщение о добавлении/удалении подписки."""

        url = reverse("users:subscription")
        data = {"users": self.user.pk, "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Подписка оформлена", response.data["message"])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Подписка отменена", response.data["message"])

    def test_get_subscription_with_right_error(self):
        """Тест проверяет работу контроллера SubscriptionAPIView без права на добавление/удаление подписки на курс.
        Проверяется корректный возврат статуса 403 и сообщение об ошибке."""

        url = reverse("users:subscription")
        group = Group.objects.create(name="moderator")
        self.user.groups.add(group)
        data = {"users": self.user.pk, "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("You do not have permission to perform this action.", response.data["detail"])

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    """Класс описывает тесты для модели Lesson."""

    def setUp(self):
        """Метод для создания первичных данных: пользователь, курс, урок, токен авторизации."""

        self.user = User.objects.create(email="admin@mail.ru")
        self.course = Course.objects.create(name="Test Course", description="Test", amount=1000)
        self.lesson = Lesson.objects.create(name="Test Lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест проверяет работу контроллера LessonRetrieveAPIView получения данных урока. Проверяется корректный
        возврат статуса 200 и названия урока."""

        url = reverse("materials:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тест проверяет работу контроллера LessonCreateAPIView создания урока. Проверяется корректный возврат
        статуса 201 и количество уроков в тестовой базе данных(2)."""

        url = reverse("materials:lesson_create")
        data = {"name": "Test Lesson №2", "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_create_with_url(self):
        """Тест проверяет работу контроллера LessonCreateAPIView создания урока с указанием youtube ссылки. Проверяется
        корректный возврат статуса 201 и количество уроков в тестовой базе данных(2)."""

        url = reverse("materials:lesson_create")
        self.course = Course.objects.create(name="Course №2", amount=500)
        data = {
            "name": "Test Lesson №3",
            "video_url": "https://www.youtube.com/watch?v=HjpNOudWFj4",
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_create_with_error_url(self):
        """Тест проверяет работу контроллера LessonCreateAPIView создания урока с указанием некорректной ссылки.
        Проверяется корректный возврат статуса 400 и сообщение ошибки."""

        url = reverse("materials:lesson_create")
        self.course = Course.objects.create(name="Course №3", amount=500)
        data = {
            "name": "Test Lesson №3",
            "video_url": "https://yandex.ru/",
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Некорректная ссылка на ресурс. Необходимо указать ссылку на youtube.com.",
            response.data["non_field_errors"]
        )

    def test_lesson_create_with_right_error(self):
        """Тест проверяет работу контроллера LessonCreateAPIView без права на создание урока. Проверяется корректный
        возврат статуса 403 и сообщение об ошибке."""

        url = reverse("materials:lesson_create")
        group = Group.objects.create(name="moderator")
        self.user.groups.add(group)
        self.course = Course.objects.create(name="Course №4", amount=500)
        data = {"name": "Test Lesson №3", "course": self.course.pk, "owner": self.user}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("You do not have permission to perform this action.", response.data["detail"])

    def test_lesson_update(self):
        """Тест проверяет работу контроллера LessonUpdateAPIView обновления данных об уроке. Проверяется корректный
        возврат статуса 200 и обновленное названия урока."""

        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "New lesson name",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "New lesson name")

    def test_lesson_delete(self):
        """Тест проверяет работу контроллера LessonDestroyAPIView удаления урока. Проверяется корректный возврат
        статуса 204 и количество уроков в базе данных(0)."""

        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест проверяет работу контроллера LessonListAPIView вывода списка уроков. Проверяется корректный возврат
        статуса 200 и список уроков с пагинацией."""

        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "description": None,
                    "video_url": None,
                    "name": self.lesson.name,
                    "preview": None,
                    "course": self.course.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class CourseTestCase(APITestCase):
    """Класс описывает тесты для модели Course."""

    def setUp(self):
        """Метод для создания первичных данных: пользователь, курс, урок, токен авторизации."""

        self.user = User.objects.create(email="admin@mail.ru")
        self.course = Course.objects.create(name="Python Course", amount=1000, owner=self.user)
        self.lesson = Lesson.objects.create(name="Git lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        """Тест проверяет работу контроллера CourseViewSet создания курса. Проверяется корректный возврат
        статуса 201 и количество курсов в тестовой базе данных(2)."""

        url = reverse("materials:course-list")
        data = {"name": "Java Course", "description": "It's a java course", "amount": 1000}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_create_with_error_description(self):
        """Тест проверяет работу контроллера CourseViewSet создания курса с указанием некорректного описания.
        Проверяется корректный возврат статуса 400 и сообщение ошибки."""

        url = reverse("materials:course-list")
        data = {"name": "Java Course", "description": "It's a java course https://yandex.ru/", "amount": 1000}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Некорректная ссылка на ресурс. Необходимо указать ссылку на youtube.com.",
            response.data["non_field_errors"]
        )

    def test_course_create_with_right_error(self):
        """Тест проверяет работу контроллера CourseViewSet без права на создание курса. Проверяется корректный
        возврат статуса 403 и сообщение об ошибке."""

        url = reverse("materials:course-list")
        group = Group.objects.create(name="moderator")
        self.user.groups.add(group)
        data = {"name": "Java Course", "amount": 100}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("You do not have permission to perform this action.", response.data["detail"])

    def test_course_retrieve(self):
        """Тест проверяет работу контроллера CourseViewSet получения данных курса. Проверяется корректный
        возврат статуса 200 и названия курса."""

        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_update(self):
        """Тест проверяет работу контроллера CourseViewSet обновления данных о курсе. Проверяется корректный
        возврат статуса 200 и обновленное названия курса."""

        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "New Course",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "New Course")

    def test_course_delete(self):
        """Тест проверяет работу контроллера CourseViewSet удаления курса. Проверяется корректный возврат
        статуса 204 и количество курсов в базе данных(0)."""

        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    # def test_course_list(self):
    #     """Тест проверяет работу контроллера CourseViewSet вывода списка курсов. Проверяется корректный возврат
    #     статуса 200 и список курсов с пагинацией."""
    #
    #     url = reverse("materials:course-list")
    #     response = self.client.get(url)
    #     data = response.json()
    #     print(data)
    #     result = {
    #         "count": 1,
    #         "next": None,
    #         "previous": None,
    #         "results": [
    #             {
    #                 "id": self.course.pk,
    #                 "lesson_count": Lesson.objects.all().count(),
    #                 "subscription": False,
    #                 "lessons": [
    #                     {
    #                         "id": self.lesson.pk,
    #                         "name": self.lesson.name,
    #                         "description": None,
    #                         "preview": None,
    #                         "video_url": None,
    #                         "course": self.course.pk,
    #                     }
    #                 ],
    #                 "name": self.course.name,
    #                 "preview": None,
    #                 "description": None,
    #                 "amount": self.course.amount,
    #                 "updated_at": self.course.updated_at
    #             }
    #         ],
    #     }
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data, result)

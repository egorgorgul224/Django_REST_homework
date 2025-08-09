from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.paginators import CourseLessonListPaginator
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Класс ViewSet модели Course для создания и удаления курса, вывода списка курсов и информации о каждом курсе."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CourseLessonListPaginator

    def perform_create(self, serializer):
        """Функция добавляет в поле owner пользователя, который создает курс."""

        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """Функция для проверки прав у пользователя. Если у пользователя есть группа прав 'Модератор', то пользователь
        может обновлять и просматривать курсы, но не может создавать или удалить их."""

        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModerator,
            )
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (IsAuthenticated, IsModerator | IsOwner)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, ~IsModerator | IsOwner)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """Класс generics модели Lesson для создания урока."""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """Функция добавляет в поле owner пользователя, который создает урок."""

        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Класс generics модели Lesson для вывода списка уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CourseLessonListPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Класс generics модели Lesson для вывода информации об уроке."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Класс generics модели Lesson для обновления информации об уроке."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Класс generics модели Lesson для удаления урока."""

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]

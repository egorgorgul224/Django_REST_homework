from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.paginators import CourseLessonListPaginator
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="Класс ViewSet модели Course для отображения списка курсов."),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(operation_description="Класс ViewSet модели Course для создания курса."),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Класс ViewSet модели Course для отображения информации о курсе."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Класс ViewSet модели Course для обновления информации о курсе."
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Класс ViewSet модели Course для обновления информации о курсе."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Класс ViewSet модели Course для удаления курса."),
)
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

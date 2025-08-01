from rest_framework import generics, viewsets

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Класс ViewSet модели Course для создания и удаления курса, вывода списка курсов и информации о каждом курсе."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """Класс generics модели Lesson для создания урока."""

    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """Класс generics модели Lesson для вывода списка уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Класс generics модели Lesson для вывода информации об уроке."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Класс generics модели Lesson для обновления информации об уроке."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Класс generics модели Lesson для удаления урока."""

    queryset = Lesson.objects.all()

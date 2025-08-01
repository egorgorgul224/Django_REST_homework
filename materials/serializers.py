from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализация модели Course. Используются все поля."""

    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        """Метод для подсчета количества уроков в курсе. 'lessons' - related_name поля 'course' модели Lesson."""

        return obj.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация модели Lesson. Используются все поля."""

    class Meta:
        model = Lesson
        fields = "__all__"

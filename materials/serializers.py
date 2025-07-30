from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализация модели Course. Используются все поля."""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация модели Lesson. Используются все поля."""

    class Meta:
        model = Lesson
        fields = "__all__"

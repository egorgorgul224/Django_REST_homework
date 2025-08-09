from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import DescriptionValidator, VideoValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация модели Lesson. Используются все поля."""

    description = serializers.CharField(validators=[DescriptionValidator()], required=False)
    video_url = serializers.CharField(validators=[VideoValidator()], required=False)

    class Meta:
        model = Lesson
        exclude = ["owner"]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализация модели Course. Используются все поля."""

    description = serializers.CharField(validators=[DescriptionValidator()], required=False)
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, obj):
        """Метод для подсчета количества уроков в курсе. 'lessons' - related_name поля 'course' модели Lesson."""

        return obj.lessons.count()

    class Meta:
        model = Course
        exclude = ["owner"]

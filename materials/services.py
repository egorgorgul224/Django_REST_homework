from django.shortcuts import get_object_or_404
from django.utils import timezone

from materials.models import Course


def get_course_last_update(course_pk):
    """Функция для получения даты последнего обновления курса."""

    course = get_object_or_404(Course, pk=course_pk)
    return course.updated_at


def get_course_info(course_pk):
    """Функция для получения информации о курсе(id курса и его название)."""

    course = get_object_or_404(Course, pk=course_pk)
    return course.pk, course.name


def update_course_time_by_lesson(course_pk):
    """Функция для изменения даты обновления курса во время обновления данных по уроку. После обновления данных по
    уроку в курсе дата последнего обновления меняется на текущую дату. Функция возвращает эту дату."""

    course = get_object_or_404(Course, pk=course_pk)
    course.updated_at = timezone.now()
    course.save()
    return course.updated_at


def is_last_update_later_4_hours(last_update, new_update):
    """Функция проверяет, что последнее обновление курса было больше 4 часов назад. Если больше, возвращает True,
    иначе возвращает False."""

    time_delta = (new_update - last_update).total_seconds() / 3600
    if time_delta > 4.0:
        return True
    return False

from django.contrib import admin

from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Админ панель по курсам. Поля для отображения: name, description. Поле для фильтра: name. Поле для поиска:
    name."""

    list_display = ("name", "description")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Админ панель по урокам. Поля для отображения: name, description, course. Поля для фильтра: name, course. Поля
    для поиска: name, course."""

    list_display = ("name", "description", "course")
    list_filter = ("name", "course")
    search_fields = ("name", "course")

from django.db import models


# Create your models here.
class Course(models.Model):
    """Модель учебного курса. Содержит поля name, preview(изображение/превью курса), description."""

    name = models.CharField(max_length=50, verbose_name="Название курса")
    preview = models.ImageField(upload_to="previews/", verbose_name="Превью курса", blank=True, null=True)
    description = models.TextField(null=True, blank=True, verbose_name="Описание курса")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["id"]


class Lesson(models.Model):
    """Модель урока. Содержит поля name, description, preview(изображение/превью курса), video_url(ссылка на видео)."""

    name = models.CharField(max_length=50, verbose_name="Название урока")
    description = models.TextField(null=True, blank=True, verbose_name="Описание урока")
    preview = models.ImageField(upload_to="previews/", verbose_name="Превью урока", blank=True, null=True)
    video_url = models.URLField(verbose_name="Видео урока", blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="courses", verbose_name="Курс")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["id"]

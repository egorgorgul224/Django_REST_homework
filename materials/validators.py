import re

from rest_framework.serializers import ValidationError


class VideoValidator:
    """Класс-валидатор для проверки ссылки на видео урока. Если ссылка ведет на любой ресурс, кроме youtube.com, то
    возбуждается ошибка: 'Некорректная ссылка на ресурс. Необходимо указать ссылку на youtube.com.'"""

    def __call__(self, field):
        pattern_url = re.compile(r"https?://(www\.)?youtube\.com/watch\?v=([0-9A-Za-z_-]{11})$")
        video_url = field.lower()
        if not video_url:
            return
        if not bool(re.match(pattern_url, video_url)):
            raise ValidationError("Некорректная ссылка на ресурс. Необходимо указать ссылку на youtube.com.")


class DescriptionValidator:
    """Класс-валидатор для проверки ссылок в описании курса и урока. Если ссылка ведет на любой ресурс, кроме
    youtube.com, то возбуждается ошибка: 'Некорректная ссылка на ресурс. Необходимо указать ссылку на youtube.com.'"""

    def __call__(self, field):
        pattern_url = re.compile(r"https?://[^\s]+")
        pattern_youtube_url = re.compile(r"https?://(www\.)?youtube\.com/.*")
        description = field.lower()
        if not description:
            return
        urls_in_des = pattern_url.findall(description)
        for url in urls_in_des:
            if not bool(re.fullmatch(pattern_youtube_url, url)):
                raise ValidationError("Некорректная ссылка на ресурс. Необходимо указать ссылку на youtube.com.")

import re

from rest_framework.serializers import ValidationError


class VideoValidator:
    """Класс-валидатор для проверки ссылки на видео урока. Если ссылка ведет на любой ресурс, кроме youtube.com, то
    возбуждается ошибка: 'Некорректная ссылка на ресурс. Необходимо указать ссылку на youtube.com.'"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern_url = re.compile(r"https?://(www\.)?youtube\.com/watch\?v=([0-9A-Za-z_-]{11})$")
        video_url = dict(value).get(self.field)
        if not video_url:
            return
        if not bool(re.match(pattern_url, video_url)):
            raise ValidationError("Некорректная ссылка на ресурс. Необходимо указать ссылку на youtube.com.")


class DescriptionValidator:
    """Класс-валидатор для проверки ссылок в описании курса и урока. Если ссылка ведет на любой ресурс, кроме
    youtube.com, то возбуждается ошибка: 'Некорректная ссылка на ресурс. Необходимо указать ссылку на youtube.com.'"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern_url = re.compile(r"https?://[^\s]+")
        pattern_youtube_url = re.compile(r"https?://(www\.)?youtube\.com/.*")
        description = dict(value).get(self.field)
        if not description:
            return
        urls_in_des = pattern_url.findall(description)
        for url in urls_in_des:
            if not bool(re.fullmatch(pattern_youtube_url, url)):
                raise ValidationError("Некорректная ссылка на ресурс. Необходимо указать ссылку на youtube.com.")

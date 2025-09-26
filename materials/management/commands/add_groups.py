from django.contrib.auth.models import Group
from django.core.management import CommandError, call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Команда для добавления групп в базу данных."

    def handle(self, *args, **kwargs):
        Group.objects.all().delete()

        try:
            call_command(
                "loaddata",
                ("group_fixture.json",),
            )
            self.stdout.write(self.style.SUCCESS("Успешно загружены данные из фикстуры."))
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f"Ошибка загрузки фикстур: {e}."))

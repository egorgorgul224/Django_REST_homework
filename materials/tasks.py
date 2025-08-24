from datetime import date, timedelta

from celery import shared_task
from django.core.mail import send_mail

from config import settings
from users.models import Subscription, User


@shared_task
def update_course_mailing(course_pk, course_name, lesson_name=None):
    """Функция для отправки сообщения об обновлении курса для всех пользователей, подписанных на данный курс."""

    email_list = []
    subs = Subscription.objects.filter(course=course_pk)
    for sub in subs:
        email_list.append(sub.user.email)
    subject = f"Обновление курса {course_name}"
    if lesson_name:
        text = f"Добрый день, в курсе {course_name} произошли изменения в уроке {lesson_name}."
    else:
        text = f"Добрый день, в курсе {course_name} произошли изменения."
    send_mail(
        subject=subject,
        message=text,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email_list,
        fail_silently=True,
    )
    print(f"Успешно отправлено на почты {email_list}")


@shared_task
def check_users_activity():
    """Функция раз в 14 дней проверяет всех пользователей по дате последнего входа на аккаунт. Если пользователь не
    заходил более месяца, то блокирует его с помощью флага is_active(флаг принимает значение False)."""

    blocked_users = []
    users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False, last_login__isnull=False)
    time_delta = timedelta(31)
    date_block = date.today() - time_delta
    for user in users:
        if user.last_login.date() <= date_block:
            user.is_active = False
            user.save()
            blocked_users.append(user.email)
    print(f"Заблокированные пользователи: {blocked_users}")

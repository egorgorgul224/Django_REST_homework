from celery import shared_task
from django.core.mail import send_mail

from config import settings
from users.models import Subscription


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

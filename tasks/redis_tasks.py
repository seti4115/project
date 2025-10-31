from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from config.celery import celery_cache
from config.settings import EMAIL_HOST_USER

User = get_user_model()

@celery_cache.task
def send_email(subject, message,to ,from_email=EMAIL_HOST_USER):
    if to:
        return send_mail(
            subject,
            message,
            from_email,
            [to],
            fail_silently=False,
        )

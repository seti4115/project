from config.celery import app
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from config.settings import EMAIL_HOST_USER

User = get_user_model()

@app.task
def send_email(subject, message,to ,from_email=EMAIL_HOST_USER):
    if to:
        return send_mail(
            subject,
            message,
            from_email,
            [to],
            fail_silently=False,
        )

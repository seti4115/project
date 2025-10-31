from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from config.settings import EMAIL_HOST_USER

User = get_user_model()

@shared_task
def send_email(subject, message, from_email=EMAIL_HOST_USER):
    user = get_object_or_404(User, pk=int)
    if user.email:
        return send_mail(
            subject,
            message,
            from_email,
            [user.email],
            fail_silently=False,
        )
    else:
        return None
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from config.celery import app
from config.settings import EMAIL_HOST_USER

User = get_user_model()

@app.task(
bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5},
    retry_backoff=True,
    retry_jitter=True,
    time_limit=10,
    soft_time_limit=7,
    queue="cache_fast",
)
def send_email(subject, message,to ,from_email=EMAIL_HOST_USER):
    if to:
        return send_mail(
            subject,
            message,
            from_email,
            [to],
            fail_silently=False,
        )


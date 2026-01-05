from datetime import timedelta

from django.contrib.auth import get_user_model

from django.utils import timezone

from config import app
from log.models import Log

User = get_user_model()


@app.task(bind=True, queue="db_heavy")
def logs(self,
        level = None,
        views = None,
        status_code = None,
        message = None,
        action = None,
        from_user = None,
        ip_address = None,
        user_agent = None,
        object_id = None,
        exception = None
):
    Log.objects.create(
        level=level,
        views=views,
        status_code=status_code,
        message=message,
        action=action,
        from_user=from_user,
        ip_address=ip_address,
        user_agent=user_agent,
        object_id=object_id,
        exception=exception,
    )
    return "log saved"


@app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
    queue="db_heavy",)
def cleanup_old_request_logs(self, days=1):
    cutoff_date = timezone.now() - timedelta(days=days)
    Log.objects.filter(
        created_at__lt=cutoff_date
    ).delete()
    return "logs deleted"
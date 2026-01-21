import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from config import app
from easyaudit.models import RequestEvent, CRUDEvent, LoginEvent
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
User = get_user_model()


@app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
    queue="db_heavy",)
def cleanup_old_request_logs(self, days=1):
    cutoff_date = timezone.now() - timedelta(minutes=days)
    RequestEvent.objects.filter(datetime__lt=cutoff_date).all().delete()
    CRUDEvent.objects.filter(datetime__lt=cutoff_date).all().delete()
    LoginEvent.objects.filter(datetime__lt=cutoff_date).all().delete()
    return "logs deleted"
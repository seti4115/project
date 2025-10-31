# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import celery_cache, celery_db

__all__ = ("celery_db", "celery_cache")
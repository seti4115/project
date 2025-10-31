import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_db = Celery("db_tasks")
celery_db.config_from_object("django.conf:settings", namespace="CELERY_DB")

celery_cache = Celery("cache_tasks")
celery_cache.config_from_object("django.conf:settings", namespace="CELERY_CACHE")

# autodiscover
celery_db.autodiscover_tasks(["tasks"])
celery_cache.autodiscover_tasks(["tasks"])
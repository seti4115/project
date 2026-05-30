import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")

# app.conf.beat_schedule = {
#     "every_thirty_seconds": {
#         "task": "tasks.db_tasks.cleanup_old_request_logs",
#         "schedule": timedelta(seconds=15),
#         "kwargs": {
#             "days": 1,
#             "minutes": 0,
#             "seconds": 0
#         }
#     },
# }

app.autodiscover_tasks()
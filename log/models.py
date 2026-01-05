from django.db import models


class Log(models.Model):
    level = models.CharField(
        max_length=20,
        choices=[
            ("info", "Info"),
            ("warning", "Warning"),
            ("error", "Error"),
            ("critical", "Critical"),
        ],
        default="info",
        db_index=True,
    )
    views = models.CharField(max_length=120)
    status_code = models.CharField(max_length=120)
    message = models.TextField()
    action = models.CharField(max_length=120, blank=True)
    from_user = models.CharField(max_length=120, blank=True, null=True)
    to_user = models.CharField(max_length=120, blank=True, null=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.CharField(max_length=100 ,blank=True, null=True)
    object_id = models.CharField(max_length=20 ,null=True, blank=True, db_index=True)
    exception = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "لاگ"
        verbose_name_plural = "لاگ ها"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["level"]),
            models.Index(fields=["created_at"]),
        ]

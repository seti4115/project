from django.utils.timezone import now
from rest_framework.exceptions import Throttled
from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle, BaseThrottle, SimpleRateThrottle

from request.models import SprayingRequest, ConsultingRequest


class DailyPostThrottle(SimpleRateThrottle):
    scope = 'daily_post'

    def get_cache_key(self, request, view):
        """
        بر اساس کاربر لاگین یا IP آدرس برای مهمان‌ها throttle بساز
        """
        if request.method != 'POST':
            # فقط برای POST محدودیت بذار
            return None

        if request.user.is_authenticated:
            ident = f"user-{request.user.id}"
        else:
            ident = self.get_ident(request)  # یعنی IP آدرس

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
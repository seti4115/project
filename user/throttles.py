from django.utils.timezone import now
from rest_framework.exceptions import Throttled
from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle, BaseThrottle, SimpleRateThrottle

from request.models import SprayingRequest, ConsultingRequest


class TenPerMinutePostThrottle(SimpleRateThrottle):
    scope = 'ten_per_minute'

    def get_cache_key(self, request, view):
        if request.method != 'POST':
            return None

        if request.user.is_authenticated:
            ident = f"user-{request.user.id}"
        else:
            ident = self.get_ident(request)  # IP

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
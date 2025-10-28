from rest_framework.exceptions import Throttled
from rest_framework.throttling import AnonRateThrottle

class DailyPostThrottle(AnonRateThrottle):
    scope = 'daily_post'

    def throttle_failure(self):
        raise Throttled(detail="شما فقط ۵ بار در روز می‌توانید درخواست ثبت کنید. لطفاً فردا دوباره امتحان کنید.")
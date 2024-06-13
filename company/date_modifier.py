from datetime import datetime

from django.utils import timezone
from workdays import workday


class DateModifier:
    @classmethod
    def get_future_date(cls, date: datetime, workdays: int) -> datetime:
        future_date = workday(date, workdays)
        future_date = future_date.replace(hour=23, minute=59, second=0)
        local_future_date = timezone.localtime(timezone.make_aware(future_date))
        return local_future_date

    @classmethod
    def get_future_date_with_limit_date(
        cls, date: datetime, workdays: int, limit_date: datetime
    ) -> datetime:
        future_date = cls.get_future_date(date, workdays)
        return future_date if not limit_date else min(future_date, limit_date)

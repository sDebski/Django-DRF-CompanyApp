from datetime import datetime, timedelta

from django.test import TestCase
from django.utils.timezone import localtime

from company.date_modifier import DateModifier


class DateModifierTestCase(TestCase):
    def setUp(self) -> None:
        self.now = datetime.now()
        return super().setUp()

    def _test_dates(self, date, expected):
        self.assertEqual(date.hour, 23)
        self.assertEqual(date.minute, 59)
        self.assertEqual(date.second, 0)
        self.assertEqual(date.date(), expected.date())

    def _get_last_busy_day(self, date):
        return date - timedelta(days=date.weekday()) if date.weekday() > 4 else date

    def test_get_dates_of_expiration_on_creation(self):
        date_after_20_busy_days = self._get_last_busy_day(
            localtime() + timedelta(weeks=4)
        )
        date_after_60_busy_days = self._get_last_busy_day(
            localtime() + timedelta(weeks=12)
        )
        expired_at = DateModifier.get_future_date(self.now, 20)
        maximum_expired_at = DateModifier.get_future_date(self.now, 60)

        self._test_dates(expired_at, date_after_20_busy_days)
        self._test_dates(maximum_expired_at, date_after_60_busy_days)

    def test_get_dates_with_limit_date(self):
        date_after_10_busy_days = self._get_last_busy_day(
            localtime() + timedelta(weeks=2)
        ).replace(hour=23, minute=59, second=0)

        expired_at = DateModifier.get_future_date_with_limit_date(
            self.now, 20, date_after_10_busy_days
        )
        self._test_dates(expired_at, date_after_10_busy_days)

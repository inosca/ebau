from datetime import datetime, timedelta

from faker.providers.date_time import Provider


class FreezegunAwareDatetimeProvider(Provider):
    """
    Workaround where datetime faker does not use frozen time of freezegun.

    Reason is that freezegun currently does not support custom date
    time classes which faker uses.

    See https://github.com/spulec/freezegun/issues/243
    """

    def past_datetime(self, tzinfo=None):
        start_date = datetime.now() - timedelta(days=30 * 365)
        end_date = datetime.now() - timedelta(seconds=1)
        return super().date_time_between(start_date, end_date, tzinfo)

    def future_datetime(self, tzinfo=None):
        start_date = datetime.now() + timedelta(seconds=1)
        end_date = datetime.now() + timedelta(days=30)
        return super().date_time_between(start_date, end_date, tzinfo)

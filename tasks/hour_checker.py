from mock import Mock, patch
from datetime import datetime
import time

from djangoCeleryTest.settings import (
    MINUTE_15,
    MINUTE_30,
    MINUTE_45,
    MINUTE_60,
    QUEUE_15,
    QUEUE_30,
    QUEUE_45,
    QUEUE_60,
)

mock_time = Mock()
mock_time.return_value = time.mktime(datetime(2022, 12, 12, 20, 16, 10).timetuple())


# @patch('time.time', mock_time)
def time_checker(time_to_check=None):
    if not time_to_check:
        return False

    time_to_check = datetime.today()
    minute_now = time_to_check.minute

    if minute_now in MINUTE_15:
        return QUEUE_15
    elif minute_now in MINUTE_30:
        return QUEUE_30
    elif minute_now in MINUTE_45:
        return QUEUE_45
    elif minute_now in MINUTE_60:
        return QUEUE_60
    else:
        return False

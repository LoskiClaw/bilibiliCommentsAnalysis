import time
import datetime
def datetime_to_timestamp_in_milliseconds(d):
    """
    todo : 时间戳
    :param d:
    :return:
    """

    def current_milli_time():
        return int(round(time.time() * 1000))

    return current_milli_time()
print(datetime_to_timestamp_in_milliseconds(datetime.datetime.now()))
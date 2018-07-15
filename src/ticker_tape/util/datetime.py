from datetime import datetime
from dateutil import tz
from dateutil.parser import parse


def datetime_to_epoch_ms(datestring):
    parsed_date = parse(datestring)
    parsed_date = parsed_date.astimezone(tz.tzutc())
    parsed_date = parsed_date.replace(tzinfo=None)
    return int((parsed_date - datetime(1970, 1, 1)).total_seconds()) * 1000
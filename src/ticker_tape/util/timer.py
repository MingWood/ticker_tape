import time


class Timer(object):
    @classmethod
    def get_current_epoch_ms(cls, tz=None):
        return int(time.time()) * 1000

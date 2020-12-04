import datetime
import time

FULL_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def formatTimestamp(timestamp, fmt=None):
    if fmt is None:
        fmt = FULL_DATE_FORMAT
    if isinstance(timestamp, int):
        return datetime.datetime.utcfromtimestamp(timestamp).strftime(fmt)
    elif isinstance(timestamp, datetime.datetime):
        return timestamp.strftime(fmt)
    else:
        raise RuntimeException(f'Unknown timestamp {timestamp}')


class NowDelta:
    def __init__(self, dt=None, default_fmt=None):
        if dt is None:
            self._now = datetime.datetime.now()
        else:
            if isinstance(dt, int):
                self._now = datetime.datetime.utcfromtimestamp(dt)
            elif isinstance(dt, datetime.datetime):
                self._now = dt
            else:
                raise RuntimeException(f'Unknown datetime {dt}')
        self._default_fmt = default_fmt

    def _Format(self, dt, fmt=None):
        fmt = fmt or self._default_fmt
        if fmt or self._default_fmt:
            return formatTimestamp(dt, fmt=fmt)
        else:
            return dt

    def Before(self, fmt=None, **kwargs):
        dt = self._now - datetime.timedelta(**kwargs)
        return self._Format(dt, fmt=fmt)

    def Now(self, fmt=None):
        dt = self._now
        return self._Format(dt, fmt=fmt)

    def After(self, fmt=None, **kwargs):
        dt = self._now + datetime.timedelta(**kwargs)
        return self._Format(dt, fmt=fmt)

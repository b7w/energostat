import logging
from collections import OrderedDict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def time_hours():
    d = datetime.strptime('01:00', '%H:%M')
    for _ in range(23):
        yield d
        d += timedelta(hours=1)
    yield datetime.strptime('00:00', '%H:%M')


def _drop_duplicates(values):
    previous = None
    for v in values:
        if previous != v._replace(number=None, utc=None):
            yield v
        else:
            logger.warning('Found duplicate metric %s, previous %s', v, previous)
        previous = v._replace(number=None, utc=None)


def _fill_missing(values):
    values = list(values)
    res = OrderedDict()
    for t in time_hours():
        res[t] = None

    for v in values:
        res[v.time] = v

    previous = values[0]
    for k, v in res.items():
        if v:
            previous = v
        else:
            new = previous._replace(time=k)
            res[k] = new
            logger.warning('Create metric %s from previous %s', new, previous)
    return res.values()


def fix_data(sensor_set):
    """
    Remove duplicates and add missing records
    """
    for sensor, values in sensor_set:
        values = list(values)
        values = _drop_duplicates(values)
        values = _fill_missing(values)
        yield sensor, values

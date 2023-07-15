import functools
import logging
import os
from collections import OrderedDict
from datetime import datetime, timedelta
from time import perf_counter

from gunicorn.app.base import BaseApplication

logger = logging.getLogger(__name__)


class GunicornApplication(BaseApplication):

    def init(self, parser, opts, args):
        pass

    def __init__(self, app, logging_dict):
        self.app = app
        self.logging_dict = logging_dict
        super(GunicornApplication, self).__init__()

    def load_config(self):
        port = os.environ.get('APP_PORT') or os.environ.get('PORT') or '5000'
        self.cfg.set('bind', f'0.0.0.0:{port}')
        self.cfg.set('workers', '1')
        self.cfg.set('logconfig_dict', self.logging_dict)

    def load(self):
        return self.app.wsgi_app


def time_hours():
    d = datetime.strptime('01:00', '%H:%M')
    for _ in range(23):
        yield d
        d += timedelta(hours=1)
    yield datetime.strptime('00:00', '%H:%M')


def _drop_duplicates(values):
    ressult = []
    report = []
    p = None
    p_full = None
    for v in values:
        if p != v._replace(number=None, utc=None):
            ressult.append(v)
        else:
            logger.warning('Found duplicate metric, ignoring. metric: %s, previous: %s', v, p_full)
            report.append(f'Найден и проигнорирован дубликат.'
                          f' Sensor: {v.sensor}, number: {v.number},'
                          f' date: {str(v.datetime)}, previous: {p_full.number}.')
        p = v._replace(number=None, utc=None)
        p_full = v
    return ressult, report


def _fill_missing(values):
    result = OrderedDict()
    report = []
    for t in time_hours():
        result[t] = None

    for v in values:
        result[v.time] = v

    previous = values[0]
    for k, v in result.items():
        if v:
            previous = v
        else:
            new = previous._replace(number=str(int(previous.number) + 2), time=k)
            result[k] = new
            logger.warning('Fill missing metric %s from previous %s', new, previous)
            report.append(f'Найдент пропуск, заполнен из предыдушего.'
                          f' Sensor: {new.sensor}, number: {new.number},'
                          f' date: {str(new.datetime)}, previous: {previous.number}.')
            previous = new
    return result.values(), report


def fix_data(sensor_set):
    """
    Remove duplicates and add missing records
    """
    result = []
    report = []
    for sensor, values in sensor_set:
        values, duplicates = _drop_duplicates(values)
        values, created = _fill_missing(values)
        result.append((sensor, values,))
        report.extend(duplicates)
        report.extend(created)
    return result, report


def timeit(f):
    msg = '## {0} complete in {1:.0f} min {2:.1f} sec ({3}pc)'

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return f(*args, **kwargs)
        finally:
            elapsed = perf_counter() - start
            elapsed_sec = elapsed / 10 ** 9

            print(msg.format(f.__name__, elapsed_sec // 60, elapsed_sec % 60, elapsed))

    return wrapper

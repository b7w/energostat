import logging
from collections import OrderedDict
from datetime import datetime, timedelta

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
        self.cfg.set('bind', '0.0.0.0:5000')
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
            logger.warning('Found duplicate metric %s, previous %s', v, p_full)
            report.append(f'Found duplicate metric sensor: {v.sensor}, number: {v.number}, previous: {p_full.number}')
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
            new = previous._replace(time=k)
            result[k] = new
            logger.warning('Create metric %s from previous %s', new, previous)
            report.append(f'Create metric sensor: {new.sensor}, number: {new.number}')
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

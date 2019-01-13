from collections import namedtuple
from datetime import timedelta

Metric = namedtuple('Metric', [
    'sensor',
    'number',
    'power_plus', 'power_minus', 'reactive_power_plus', 'reactive_power_minus',
    'datetime', 'time', 'date', 'period', 'desc', 'utc'
])


def key_date(p: Metric):
    return (p.datetime - timedelta(seconds=1)).date()


def key_sensor(p: Metric):
    return p.sensor

from collections import namedtuple

Metric = namedtuple('Metric', [
    'sensor',
    'number',
    'power_plus', 'power_minus', 'reactive_power_plus', 'reactive_power_minus',
    'time', 'date', 'period', 'desc', 'utc'
])


def key_date(p: Metric):
    return p.date


def key_sensor(p: Metric):
    return p.sensor

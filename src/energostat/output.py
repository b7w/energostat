from datetime import datetime, timedelta
from decimal import Decimal
from zipfile import ZipFile

from lxml import etree
from lxml.builder import E

from energostat.model import Metric

FORMAT_TIMESTAMP = '%Y%m%d%H%M%S'
FORMAT_DAY = '%Y%m%d'
FORMAT_HM = '%H%M'


def format_decimal(value: Decimal):
    v = value.to_integral() if value == value.to_integral() else value.normalize()
    return str(v).replace('.', ',')


def period_el(metric: Metric):
    start = metric.time - timedelta(hours=1)
    return (
        E.period(
            dict(start=start.strftime(FORMAT_HM), end=metric.time.strftime(FORMAT_HM)),
            E.value(
                dict(status='0'),
                format_decimal(metric.power_plus)
            )
        )
    )


def account_point_el(agreement_id, point, periods):
    return (
        E.accountpoint(
            dict(code=agreement_id + point, name=''),
            E.measuringchannel(
                dict(code="01", desc="показание активного приема"),
                *periods
            )
        )
    )


def create_xml(agreement_id, sender_inn, sender_name, date, sensor_set):
    account_points = []
    for sensor, values in sensor_set:
        periods = [period_el(i) for i in values]
        if len(periods) != 24:
            raise Exception(f'Sensor {sensor} has {len(periods)} periods for date {date}')
        ap = account_point_el(agreement_id, sensor, periods)
        account_points.append(ap)

    tree = (
        E.message(
            {'class': '80020', 'version': '2', 'number': '2'},
            E.datetime(
                E.timestamp(datetime.now().strftime(FORMAT_TIMESTAMP)),
                E.daylightsavingtime('1'),
                E.day(date.strftime(FORMAT_DAY))
            ),
            E.sender(
                E.inn(sender_inn),
                E.name(sender_name)
            ),
            E.area(
                dict(timezone='1'),
                E.inn('0000000000'),
                E.name('0'),
                *account_points
            )
        )
    )
    return etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='windows-1251', standalone=True)


def create_zip(file, messages):
    with ZipFile(file, 'w') as z:
        for name, xml in messages:
            z.writestr(f'{name}.xml', xml)

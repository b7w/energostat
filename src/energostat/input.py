import logging
from datetime import datetime
from decimal import Decimal
from zipfile import ZipFile

import toml as toml
from parsel import Selector

from energostat.model import Metric

logger = logging.getLogger(__name__)


def read_zip(file):
    html = []
    settings = {}
    with ZipFile(file) as z:
        for name in z.namelist():
            if name.endswith('.html'):
                s = str(z.read(name), encoding='cp1251')
                logger.info('Load %s', name)
                html.append((name, s,))
            if name.endswith('.ini'):
                s = str(z.read(name), encoding='utf8')
                logger.info('Load %s', name)
                settings = toml.loads(s)
    return settings, html


def read_html(sources):
    for name, src in sources:
        sel = Selector(text=src)
        sensor = sel.css('h2').re_first(r'.*Серийный\s+номер\s+-\s+(\w+).*')
        if not sensor:
            raise Exception(f'В файле {name} не найден серийный номер')
        logger.info('Find sensor %s in %s', sensor, name)
        rows = sel.css('tbody tr')
        logger.info('Find %s rows in %s', len(rows), name)
        for row in rows:
            n, power_plus, pm, rpp, rpm, time, date, p, d, utc = (i.css('::text').get() for i in row.css('td'))
            yield (Metric(sensor, n, Decimal(power_plus), pm, rpp, rpm, datetime.strptime(time, '%H:%M'),
                          datetime.strptime(date, '%d.%m.%y').date(), p, d, utc))

import logging
from datetime import datetime
from decimal import Decimal
from pathlib import Path
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
            if not Path(name).name.startswith('.'):
                if name.endswith('.html'):
                    s = str(z.read(name), encoding='cp1251')
                    logger.info('Load %s', name)
                    html.append((name, s,))
                if not name.startswith('.') and name.endswith('.ini'):
                    r = z.read(name)
                    s = str(r, encoding='utf-8-sig')
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
            f_date = datetime.strptime(date, '%d.%m.%y').date() \
                if len(date) == 8 \
                else datetime.strptime(date, '%d.%m.%Y').date()
            full_date = datetime.strptime(date + ' ' + time, '%d.%m.%y %H:%M') \
                if len(date) == 8 \
                else datetime.strptime(date + ' ' + time, '%d.%m.%Y %H:%M')
            yield (Metric(sensor, n, Decimal(power_plus), pm, rpp, rpm, full_date, datetime.strptime(time, '%H:%M'),
                          f_date, p, d, utc))

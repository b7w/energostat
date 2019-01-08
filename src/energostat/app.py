import logging
from io import BytesIO
from itertools import groupby

from energostat.input import read_zip, read_html
from energostat.model import key_date, key_sensor
from energostat.output import create_xml, create_zip
from energostat.utils import fix_data

logger = logging.getLogger('root')


def html2xml(f_in, f_out):
    settings, sources = read_zip(f_in)
    if not settings:
        raise Exception('Не найдено settings.ini')
    if not sources:
        raise Exception('Не найдено html файлов')
    agreement_id = settings['agreement_id']
    company_inn = settings['company_inn']
    company_name = settings['company_name']
    metrics = read_html(sources)
    messages = []
    for date, v in groupby(sorted(metrics, key=key_date), key=key_date):
        sensor_set = groupby(sorted(v, key=key_sensor), key=key_sensor)
        sensor_set = fix_data(sensor_set)
        xml = create_xml(agreement_id, company_inn, company_name, date, sensor_set)
        msg = f'80020_001_{agreement_id}_{date:%d%m%Y}', xml
        logger.debug('XML: %s', msg)
        messages.append(msg)
    create_zip(f_out, messages)


def html2xml_bytes(file):
    f_in = BytesIO()
    f_out = BytesIO()

    f_in.write(file.read())
    f_in.seek(0)

    html2xml(f_in, f_out)
    f_out.seek(0)
    return f_out

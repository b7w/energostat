import re
import unittest
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from energostat.app import html2xml_bytes
from energostat.utils import timeit


class TestUtils(unittest.TestCase):
    RE_TIMESTAMP = re.compile(r'<timestamp>.*</timestamp>')

    @timeit
    def test_app(self):
        pwd = Path(__file__).parent
        f_in = self._make_zip_input(pwd)
        f_out = html2xml_bytes(f_in)
        files = self._read_zip_files(f_out)
        self.assertEqual(len(files), 32, 'File count differs')
        for name, content in files:
            from_zip = self._fix_timestamp(str(content, encoding='cp1251'))
            expect = self._fix_timestamp(Path(pwd, 'test_app.output', name).read_text('cp1251'))
            self.assertEqual(from_zip, expect, f'File {name} differs')

    def _read_zip_files(self, f):
        with ZipFile(f, mode='r') as z:
            return [(i, z.read(i)) for i in sorted(z.namelist())]

    def _make_zip_input(self, pwd):
        io = BytesIO()
        with ZipFile(io, mode='w') as z:
            z.write(Path(pwd, 'test_app.input.html'), 'sample.html')
            z.write(Path(pwd, '../static/settings.ini').resolve(), 'settings.ini')
        io.seek(0)
        return io

    def _fix_timestamp(self, text):
        return self.RE_TIMESTAMP.sub('<timestamp>0000</timestamp>', text, count=1)


if __name__ == '__main__':
    unittest.main()

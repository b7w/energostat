import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from energostat.app import html2xml_bytes
from energostat.utils import timeit


class TestUtils(unittest.TestCase):

    @timeit
    def test_app(self):
        with tempfile.NamedTemporaryFile() as tmp:
            with ZipFile(tmp.name, mode='w') as z:
                pwd = Path(__file__).parent
                z.write(Path(pwd, 'sample.html'), 'sample.html')
                z.write(Path(pwd, '../../static/settings.ini').resolve(), 'settings.ini')
            html2xml_bytes(tmp)


if __name__ == '__main__':
    unittest.main()

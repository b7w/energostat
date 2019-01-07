import unittest
from logging.config import dictConfig

from energostat.utils import _fill_missing, time_hours
from main import LOGGING


class Rec:
    def __init__(self, number, time):
        self.number = number
        self.time = time

    def _replace(self, time=None):
        return Rec(self.number, time)

    def __repr__(self):
        return f'Rec({self.number}, {self.time.time()})'

    def __eq__(self, other):
        return other and self.time == other.time

    def __hash__(self):
        return hash(self.time)


class TestUtils(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)

    def test_fill_missing(self):
        expected = list(map(lambda x: Rec(x[0], x[1]), enumerate(time_hours())))
        actual = list(_fill_missing(expected[3:6]))
        self.assertEqual(len(actual), 24)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

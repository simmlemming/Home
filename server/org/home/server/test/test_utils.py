import unittest
from org.home.server.utils import validate_update


class UtilsTest(unittest.TestCase):

    def test_validate_update_no_time(self):
        update = dict()
        self.assertFalse(validate_update(update))

    def test_validate_update_time_not_int(self):
        update = dict(time=1450656000.123, state='on', sensors=[])
        self.assertFalse(validate_update(update))

    def test_validate_update_time_before_2016(self):
        update = dict(time=1350656000, state='on', sensors=[])
        self.assertFalse(validate_update(update))

    def test_validate_update_time_after_2116(self):
        update = dict(time=4604256001, state='on', sensors=[])
        self.assertFalse(validate_update(update))

    def test_validate_update_valid(self):
        update = dict(time=1450656001, state='on', sensors=[])
        self.assertTrue(validate_update(update))

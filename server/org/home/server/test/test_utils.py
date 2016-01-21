import unittest
from org.home.server.utils import validate_update, validate_mode


class UtilsTest(unittest.TestCase):

    def test_validate_mode_no_mode(self):
        mode = dict()
        self.assertFalse(validate_mode(mode))

    def test_validate_mode_unknown_mode(self):
        mode = dict(mode='unknown_mode')
        self.assertFalse(validate_mode(mode))

    def test_validate_mode_valid_mode(self):
        self.assertTrue(validate_mode(dict(mode='guard')))
        self.assertTrue(validate_mode(dict(mode='serve')))
        self.assertTrue(validate_mode(dict(mode='off')))

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

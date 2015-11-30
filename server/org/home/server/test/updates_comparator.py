import copy
import unittest

from org.home.server.updates_comparator import Comparator


class ComparatorTest(unittest.TestCase):

    def setUp(self):
        self.update_under_test = dict(time=131, state='on', sensors=[dict(name='a', state=1)])

    def test_equals(self):
        old = self.update_under_test
        new = self.update_under_test

        result, sensors = Comparator().compare(old, new)

        self.assertEquals(Comparator.RESULT_EQUALS, result)

    def test_state_changed(self):
        old = self.update_under_test
        new = copy.deepcopy(old)
        new['state'] = 'off'

        result, data = Comparator().compare(old, new)

        self.assertEquals(Comparator.RESULT_STATE_CHANGED, result)

    def test_no_old_int_error(self):
        result, data = Comparator().compare(None, {})
        self.assertEquals(Comparator.RESULT_INTERNAL_ERROR, result)

    def test_no_new_int_error(self):
        result, data = Comparator().compare({}, None)
        self.assertEquals(Comparator.RESULT_INTERNAL_ERROR, result)

    def test_no_state_int_error(self):
        self.update_under_test.pop('state', None)
        result, data = Comparator().compare(self.update_under_test, self.update_under_test)
        self.assertEquals(Comparator.RESULT_INTERNAL_ERROR, result)

    def test_new_sensor(self):
        new = copy.deepcopy(self.update_under_test)
        new['sensors'].insert(0, dict(name='b', state=1))

        result, sensors = Comparator().compare(self.update_under_test, new)

        self.assertEquals(Comparator.RESULT_NEW_SENSOR, result)
        self.assertEquals(1, len(sensors))
        self.assertEquals(dict(name='b', state=1), sensors[0])

    def test_missing_sensor(self):
        old = copy.deepcopy(self.update_under_test)
        old['sensors'].insert(0, dict(name='b', state=1))

        result, sensors = Comparator().compare(old, self.update_under_test)

        self.assertEquals(Comparator.RESULT_MISSING_SENSOR, result)
        self.assertEquals(1, len(sensors))
        self.assertEquals(dict(name='b', state=1), sensors[0])

    def test_one_sensor_updated_state(self):
        old = self.update_under_test
        old['sensors'].insert(0, dict(name='b', state=1))
        new = copy.deepcopy(old)
        new['sensors'][0]['state'] = 0

        result, sensors = Comparator().compare(old, new)
        self.assertEquals(Comparator.RESULT_SENSORS_UPDATED, result)
        self.assertEquals(1, len(sensors))
        self.assertEquals(dict(name='b', state=0), sensors[0])

    def test_two_sensors_updated_state(self):
        old = self.update_under_test
        old['sensors'].append(dict(name='b', state=1))
        new = copy.deepcopy(old)
        new['sensors'][0]['state'] = 0
        new['sensors'][1]['state'] = 0

        result, sensors = Comparator().compare(old, new)

        self.assertEquals(Comparator.RESULT_SENSORS_UPDATED, result)
        self.assertEquals(2, len(sensors))
        self.assertEquals(dict(name='a', state=0), sensors[0])
        self.assertEquals(dict(name='b', state=0), sensors[1])


if __name__ == "__main__":
    unittest.main()

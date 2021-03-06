import org.home.server.storage as storage
import unittest
import org.home.server.utils as utils


class StorageTest(unittest.TestCase):

    def setUp(self):
        utils.rm('tmp.db')
        storage.DATABASE_FILE_NAME = 'tmp.db'

    def test_put_get_string(self):
        a = storage.get_string('a', 'default_value')
        self.assertEqual('default_value', a)

        storage.put('a', 1)
        a = storage.get_string('a', 2)
        self.assertEqual('1', a)

    def test_put_get_int(self):
        a = storage.get_int('a', 34)
        self.assertEqual(34, a)

        storage.put('a', 1)
        a = storage.get_int('a', 2)
        self.assertEqual(1, a)

    def test_token_update(self):
        device_1 = dict(device_name='d1', device_token='t1')
        device_2 = dict(device_name='d2', device_token='t2')

        storage.add_device(device_1)
        devices = storage.get_all_devices()
        self.assertEqual(1, len(devices))

        storage.add_device(device_2)
        devices = storage.get_all_devices()
        self.assertEqual(2, len(devices))

        device_1['device_token'] = 't_updated'
        storage.add_device(device_1)
        devices = storage.get_all_devices()
        self.assertEqual(2, len(devices))

        self.assertTrue(('d1', 't_updated') in devices)

    def tearDown(self):
        utils.rm('tmp.db')

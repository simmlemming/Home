import unittest
import org.home.server.request_handler as handler
import os
from unittest.mock import patch
from org.home.server.updates_comparator import Comparator


def sensor_info(name, state):
    return {'name': name,
            'state': state}


class IntegrationTest(unittest.TestCase):
    TMP_DATABASE_FILE_NAME = 'db.tmp'
    TMP_LAST_UPDATE_FILE_NAME = 'last_update.tmp'

    def setUp(self):
        handler.storage.DATABASE_FILE_NAME = IntegrationTest.TMP_DATABASE_FILE_NAME
        handler.storage.LAST_UPDATE_FILE_NAME = IntegrationTest.TMP_LAST_UPDATE_FILE_NAME
        self.__cleanup()
        self.device_1 = dict(device_name='d_1', device_token='t_1')
        self.device_2 = dict(device_name='d_2', device_token='t_2')
        self.base_update = {'time': 123,
                            'state': 'on',
                            'sensors': [
                                sensor_info('Front door', 0),
                                sensor_info('Back door', 0),
                                sensor_info('Kitchen door', 0),
                                ]
                            }

    @patch('org.home.server.updates_processor.notifier')
    def test_1(self, notifier_mock):
        handler.on_new_device(self.device_1)
        update = self.base_update

        handler.on_new_update(update)

        notifier_mock.notify.assert_not_called()

        update['state'] = 'off'
        handler.on_new_update(update)

        notifier_mock.notify.assert_called_with(Comparator.RESULT_STATE_CHANGED, update, None)

    def tearDown(self):
        self.__cleanup()

    def __cleanup(self):
        try:
            os.remove(IntegrationTest.TMP_DATABASE_FILE_NAME)
        except FileNotFoundError:
            pass

        try:
            os.remove(IntegrationTest.TMP_LAST_UPDATE_FILE_NAME)
        except FileNotFoundError:
            pass


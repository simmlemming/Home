import unittest
from unittest.mock import call
import org.home.server.request_handler as handler
import org.home.server.storage as storage
import os
from unittest.mock import patch
import org.home.server.utils as utils


def sensor_info(name, state):
    return {'name': name,
            'state': state}


class IntegrationTest(unittest.TestCase):
    TMP_DATABASE_FILE_NAME = 'db.tmp'
    TMP_LAST_UPDATE_FILE_NAME = 'last_update.tmp'

    def setUp(self):
        handler.storage.DATABASE_FILE_NAME = IntegrationTest.TMP_DATABASE_FILE_NAME
        handler.storage.LAST_UPDATE_FILE_NAME = IntegrationTest.TMP_LAST_UPDATE_FILE_NAME
        self.cleanup()
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

    @patch('org.home.server.notifier.push_sender.send_to_one', return_value=(200, None))
    def test_1(self, send_to_one_method_mock):
        handler.on_new_device(self.device_1)
        handler.on_new_device(self.device_2)
        update = self.base_update

        # Initial update
        handler.on_new_update(update)

        send_to_one_method_mock.assert_not_called()
        self.assertEqual(0, len(storage.get_log()))

        # Same state
        handler.on_new_update(update)

        send_to_one_method_mock.assert_not_called()
        self.assertEqual(0, len(storage.get_log()))

        # State changed
        update['state'] = 'off'

        handler.on_new_update(update)

        calls = [call('t_1', update), call('t_2', update)]
        send_to_one_method_mock.assert_has_calls(calls, any_order=False)
        self.assertEqual(1, len(storage.get_log()))

    def tearDown(self):
        self.cleanup()

    def cleanup(self):
        utils.rm(IntegrationTest.TMP_DATABASE_FILE_NAME)
        utils.rm(IntegrationTest.TMP_LAST_UPDATE_FILE_NAME)

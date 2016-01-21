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
        self.base_update = {'sensors': [
                                sensor_info('Front door', 0),
                                sensor_info('Back door', 0),
                                sensor_info('Kitchen door', 0),
                                ]
                            }

    @patch('org.home.server.notifier.push_sender.send_to_one', return_value=(200, None))
    @patch('org.home.server.updates_processor.current_time_s', return_value=1453306171)
    @patch('org.home.server.updates_processor.settings.get_mode', return_value='guard')
    def test_1(self, get_mode_mock, current_time_mock, send_to_one_method_mock):
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
        update['sensors'][0]['state'] = 1

        handler.on_new_update(update)

        expected_system_state = dict(update)
        expected_system_state['mode'] = 'guard'
        expected_system_state['state'] = 'alarm'

        calls = [call('t_1', expected_system_state), call('t_2', expected_system_state)]
        send_to_one_method_mock.assert_has_calls(calls, any_order=False)
        self.assertEqual(1, len(storage.get_log()))

    def tearDown(self):
        self.cleanup()

    def cleanup(self):
        utils.rm(IntegrationTest.TMP_DATABASE_FILE_NAME)
        utils.rm(IntegrationTest.TMP_LAST_UPDATE_FILE_NAME)

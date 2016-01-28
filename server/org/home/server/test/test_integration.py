import unittest
from unittest.mock import call
import org.home.server.request_handler as handler
import org.home.server.storage as storage
from unittest.mock import patch
import org.home.server.utils as utils
from org.home.server.test.test_updates_processor import update


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

    @patch('org.home.server.updates_processor.notifier')
    @patch('org.home.server.updates_processor.current_time_s', return_value=1453306171)
    @patch('org.home.server.updates_processor.settings.get_mode', return_value='guard')
    def test_alarm_flow(self, mock_get_mode, mock_current_time, mock_notifier):
        last_update = update(1, 0, 0)
        last_update['time'] = 1453306171
        storage.save_last_update(last_update)

        handler.on_new_update(update(0, 1, 0))

        expected_system_state = update(1, 1, 0)
        expected_system_state['mode'] = 'guard'
        expected_system_state['state'] = 'alarm'
        expected_system_state['time'] = 1453306171

        actual_system_state = mock_notifier.notify.call_args[0][1]
        self.assertEqual('guard', actual_system_state['mode'])
        self.assertEqual('alarm', actual_system_state['state'])
        self.assertEqual(1453306171, actual_system_state['time'])
        self.assertCountEqual(expected_system_state['sensors'], actual_system_state['sensors'])

        actual_stored_last_update = storage.get_last_update()
        expected_stored_last_update = update(1, 1, 0)

        self.assertCountEqual(expected_stored_last_update['sensors'], actual_stored_last_update['sensors'])

    @patch('org.home.server.notifier.push_sender.send_to_one', return_value=(200, None))
    @patch('org.home.server.updates_processor.current_time_s', return_value=1453306171)
    @patch('org.home.server.updates_processor.settings.get_mode', return_value='guard')
    def test_1(self, get_mode_mock, current_time_mock, send_to_one_method_mock):
        handler.on_new_device(self.device_1)
        handler.on_new_device(self.device_2)
        initial_update = update(0, 0, 0)

        # Initial update
        handler.on_new_update(initial_update)

        send_to_one_method_mock.assert_not_called()
        self.assertEqual(0, len(storage.get_log()))

        # Same state
        handler.on_new_update(initial_update)

        send_to_one_method_mock.assert_not_called()
        self.assertEqual(0, len(storage.get_log()))

        # State changed
        second_update = update(1, 0, 0)

        handler.on_new_update(second_update)

        expected_system_state = dict(second_update)
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

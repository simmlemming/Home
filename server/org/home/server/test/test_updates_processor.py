import unittest
from unittest.mock import patch
from org.home.server.updates_comparator import Comparator
import org.home.server.updates_processor as processor


class UpdatesProcessorTest(unittest.TestCase):

    @patch('org.home.server.updates_processor.storage')
    @patch('org.home.server.updates_processor.notifier')
    @patch('org.home.server.updates_processor.current_time_s', return_value=1453306171)
    def test_no_last_update(self, mock_current_time, mock_notifier, mock_storage):
        mock_storage.get_last_update.return_value = None

        processor.on_new_update(update(1, 0, 0))

        mock_notifier.notify.assert_not_called()
        mock_storage.save_last_update.assert_called_with(update(1, 0, 0, 1453306171))

    @patch.object(Comparator, 'compare', return_value=(Comparator.RESULT_EQUALS, None))
    @patch('org.home.server.updates_processor.storage')
    @patch('org.home.server.updates_processor.notifier')
    @patch('org.home.server.updates_processor.current_time_s', return_value=1453303467)
    def test_last_update_equals(self, mock_current_time, mock_notifier, mock_storage, mock_comparator):
        mock_storage.get_last_update.return_value = update(1, 0, 0, 1453303423)

        processor.on_new_update(update(1, 0, 0, 1453303424))

        mock_notifier.notify.assert_not_called()
        mock_storage.save_last_update.assert_called_with(update(1, 0, 0, 1453303467))

    @patch.object(Comparator, 'compare', return_value=(Comparator.RESULT_NEW_SENSOR, 'c'))
    @patch('org.home.server.updates_processor.storage')
    @patch('org.home.server.updates_processor.notifier')
    @patch('org.home.server.updates_processor.current_time_s', return_value=1453303467)
    @patch('org.home.server.updates_processor.settings.get_mode', return_value='guard')
    def test_new_sensor(self, mock_settings, mock_current_time, mock_notifier, mock_storage, mock_comparator):
        mock_storage.get_last_update.return_value = update(0, 0, 0, 1453303467)

        processor.on_new_update(update(0, 0, 0, 1453303469))

        expected_system_state = update(0, 0, 0, 1453303467)
        expected_system_state['time'] = 1453303467
        expected_system_state['mode'] = 'guard'
        expected_system_state['state'] = 'ok'

        expected_last_update_to_save = update(0, 0, 0, 1453303467)

        mock_notifier.notify.assert_called_with(Comparator.RESULT_NEW_SENSOR, expected_system_state)
        mock_storage.save_last_update.assert_called_with(expected_last_update_to_save)
        mock_storage.add_to_log.assert_called_with(expected_system_state)


def update(state1, state2, state3, time=None):
    sensors = [dict(name='s1', state=state1), dict(name='s2', state=state2), dict(name='s3', state=state3)]
    result = dict(sensors=sensors)

    if time:
        result['time'] = time

    return result

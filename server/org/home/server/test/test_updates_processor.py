import unittest
from unittest.mock import patch
from org.home.server.updates_comparator import Comparator
import org.home.server.updates_processor as processor


class UpdatesProcessorTest(unittest.TestCase):

    @patch('org.home.server.updates_processor.storage')
    @patch('org.home.server.updates_processor.notifier')
    @patch('org.home.server.updates_processor.current_time_s')
    def test_no_last_update(self, mock_current_time, mock_notifier, mock_storage):
        mock_current_time.return_value = 1453303467
        mock_storage.get_last_update.return_value = None

        processor.on_new_update(dict(a='a', time=1453303467))

        mock_notifier.notify.assert_not_called()
        mock_storage.save_last_update.assert_called_with(dict(a='a', time=1453303467))

    @patch.object(Comparator, 'compare', return_value=(Comparator.RESULT_EQUALS, None))
    @patch('org.home.server.updates_processor.storage')
    @patch('org.home.server.updates_processor.notifier')
    @patch('org.home.server.updates_processor.current_time_s')
    def test_last_update_equals(self, mock_current_time, mock_notifier, mock_storage, mock_comparator):
        mock_current_time.return_value = 1453303467
        mock_storage.get_last_update.return_value = dict(a='a', time=1231231)

        processor.on_new_update(dict(a='a'))

        mock_notifier.notify.assert_not_called()
        mock_storage.save_last_update.assert_called_with(dict(a='a', time=1453303467))

    @patch.object(Comparator, 'compare', return_value=(Comparator.RESULT_NEW_SENSOR, 'c'))
    @patch('org.home.server.updates_processor.storage')
    @patch('org.home.server.updates_processor.notifier')
    @patch('org.home.server.updates_processor.current_time_s')
    @patch('org.home.server.updates_processor.settings')
    def test_new_sensor(self, mock_settings, mock_current_time, mock_notifier, mock_storage, mock_comparator):
        mock_settings.get_mode.return_value = 'guard'
        mock_current_time.return_value = 1453303467
        mock_storage.get_last_update.return_value = dict(sensors=[], time=1453303467)

        processor.on_new_update(dict(sensors=[]))

        expected_system_state = dict(sensors=[], time=1453303467, mode='guard', state='ok')
        expected_last_update_to_save = dict(sensors=[], time=1453303467)

        mock_notifier.notify.assert_called_with(Comparator.RESULT_NEW_SENSOR, expected_system_state)
        mock_storage.save_last_update.assert_called_with(expected_last_update_to_save)
        mock_storage.add_to_log.assert_called_with(expected_system_state)


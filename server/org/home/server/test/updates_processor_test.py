import unittest
from unittest.mock import patch
from org.home.server.updates_comparator import Comparator
import org.home.server.updates_processor as processor


class UpdatesProcessorTest(unittest.TestCase):

    @patch('org.home.server.updates_processor.storage')
    @patch('org.home.server.updates_processor.notifier')
    def test_no_last_update(self, mock_notifier, mock_storage):
        mock_storage.get_last_update.return_value = None

        processor.on_new_update('a')

        mock_notifier.notify.assert_not_called()
        mock_storage.save_last_update.assert_called_with('a')

    @patch.object(Comparator, 'compare', return_value=(Comparator.RESULT_EQUALS, None))
    @patch('org.home.server.updates_processor.storage')
    @patch('org.home.server.updates_processor.notifier')
    def test_last_update_equals(self, mock_notifier, mock_storage, mock_comparator):
        mock_storage.get_last_update.return_value = 'b'

        processor.on_new_update('a')

        mock_notifier.notify.assert_not_called()
        mock_storage.save_last_update.assert_called_with('a')

    @patch.object(Comparator, 'compare', return_value=(Comparator.RESULT_NEW_SENSOR, 'c'))
    @patch('org.home.server.updates_processor.storage')
    @patch('org.home.server.updates_processor.notifier')
    def test_new_sensor(self, mock_notifier, mock_storage, mock_comparator):
        mock_storage.get_last_update.return_value = 'b'

        processor.on_new_update('a')

        mock_notifier.notify.assert_called_with(Comparator.RESULT_NEW_SENSOR, 'a', 'c')
        mock_storage.save_last_update.assert_called_with('a')
        mock_storage.add_to_log.assert_called_with('a')


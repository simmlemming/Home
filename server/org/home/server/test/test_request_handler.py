import unittest
import org.home.server.request_handler
from sqlite3 import OperationalError
from unittest.mock import patch


class HomeRequestHandlerTest(unittest.TestCase):

    @patch('org.home.server.request_handler.utils')
    @patch('org.home.server.request_handler.storage')
    def test_post_device_invalid_data(self, mock_storage, mock_utils):
        mock_utils.validate_device.return_value = False

        code, text = org.home.server.request_handler.on_new_device("Qwdqwd")

        self.assertFalse(mock_storage.add_device.called)
        self.assertEqual(422, code)
        self.assertEqual("Invalid device", text)

    @patch('org.home.server.request_handler.utils')
    @patch('org.home.server.request_handler.storage')
    def test_post_device_exception(self, mock_storage, mock_utils):
        mock_utils.validate_device.return_value = True
        mock_storage.add_device.side_effect = OperationalError

        code, text = org.home.server.request_handler.on_new_device("Qwdqwd")

        self.assertEqual(500, code)

    @patch('org.home.server.request_handler.notifier')
    @patch('org.home.server.request_handler.utils')
    @patch('org.home.server.request_handler.storage')
    def test_post_device_valid_data(self, mock_storage, mock_utils, mock_notifier):
        mock_utils.validate_device.return_value = True

        code, text = org.home.server.request_handler.on_new_device("Qwdqwd")

        mock_storage.add_device.assert_called_with("Qwdqwd")
        mock_notifier.notify_device_added.assert_called_with("Qwdqwd")
        self.assertEqual(200, code)
        self.assertEqual("Device added", text)

import json
import org.home.server.storage as storage
import org.home.server.notifier as notifier
import org.home.server.updates_processor as processor
from cgi import parse_header
from http.server import BaseHTTPRequestHandler
from sqlite3 import OperationalError
from org.home.server.utils import *


class HomeRequestHandler(BaseHTTPRequestHandler):

    # noinspection PyPep8Naming
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        try:
            response = str(storage.get_log())
        except OperationalError:
            self.__error_response(500, "Cannot read from database")
            return

        self.wfile.write(bytes(response, encoding='utf8'))

    # noinspection PyPep8Naming
    def do_POST(self):
        data = self.parse_POST()

        if self.path == '/device':
            code, message = self.__on_new_device(data)

        elif self.path == '/update':
            code, message = self.__on_new_update(data)

        else:
            self.__error_response(404, "")
            print('Unknown path: ' + self.path)
            return

        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(message, encoding='utf8'))

    def __on_new_device(self, token):
        if not validate_device(token):
            return 422, "Invalid device token"

        try:
            storage.add_device(token)
            notifier.notify_device_added(token)
            return 200, "Device added"

        except OperationalError as e:
            return 500, "Cannot process device: " + str(e)

    def __on_new_update(self, update):
        if not validate_update(update):
            return 422, "Invalid update"

        try:
            processor.on_new_update(update)
            return 200, "Update precessed"

        except OperationalError as e:
            return 500, "Cannot process update: " + str(e)

    def __error_response(self, error_code, message):
        self.send_response(error_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(message, encoding='utf8'))

    # noinspection PyPep8Naming
    def parse_POST(self):
        content_type, pdict = parse_header(self.headers['content-type'])

        if content_type == 'multipart/form-data':
            post_vars = "{}"

        elif content_type == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            post_vars = self.rfile.read(length).decode('ascii')
            post_vars = json.loads(post_vars)

        else:
            post_vars = "{}"

        return post_vars

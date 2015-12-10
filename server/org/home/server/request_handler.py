import json
import org.home.server.storage as storage
import org.home.server.notifier as notifier
import org.home.server.updates_processor as processor
import org.home.common.log as log
from cgi import parse_header
from http.server import BaseHTTPRequestHandler
from sqlite3 import OperationalError
import org.home.server.utils as utils


def on_new_device(token):
    if not utils.validate_device(token):
        return 422, "Invalid device"

    try:
        storage.add_device(token)
        notifier.notify_device_added(token)
        return 200, "Device added"

    except Exception as e:
        return 500, "Cannot process device: " + str(e)


def on_new_update(update):
    if not utils.validate_update(update):
        return 422, "Invalid update"

    try:
        processor.on_new_update(update)
        return 200, "Update processed"

    except OperationalError as e:
        return 500, "Cannot process update: " + str(e)


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
        data = self.parse_post()

        if self.path == '/device':
            code, message = on_new_device(data)

        elif self.path == '/update':
            code, message = on_new_update(data)

        else:
            code, message = 404, 'Unknown path: ' + self.path

        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(message, encoding='utf8'))

        log.d(message)
        if code != 200:
            log.e('%s: %s' % (code, message))

    def parse_post(self):
        content_type, pdict = parse_header(self.headers['content-type'])

        if content_type == 'application/json':
            length = int(self.headers['content-length'])
            post_vars = self.rfile.read(length).decode('utf-8')
            post_vars = json.loads(post_vars)

        else:
            post_vars = dict()

        return post_vars

    def __error_response(self, error_code, message):
        self.send_response(error_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(message, encoding='utf8'))

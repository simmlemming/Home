from http.server import HTTPServer
import org.home.common.log as log
from org.home.server.request_handler import HomeRequestHandler
import signal
import threading
import getopt
import sys


def shutdown_server(signal, frame):
    log.i('Shutting down (killed)')
    threading.Thread(daemon=True, target=server.shutdown).start()


def get_ip_from_args():
    opts, args = getopt.getopt(sys.argv[1:], "a:")

    for opt, arg in opts:
        if opt == "-a":
            return arg

    return '0.0.0.0'

IP_ADDRESS = get_ip_from_args()
IP_PORT = 8080

log.init()
signal.signal(signal.SIGTERM, shutdown_server)

server = HTTPServer((IP_ADDRESS, IP_PORT), HomeRequestHandler)
log.i('Started on {0}:{1}'.format(IP_ADDRESS, IP_PORT))

if IP_ADDRESS == '0.0.0.0':
    print('You can set an ip address by passing -a parameter: ... -a 127.0.0.1')

try:
    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    log.i('Shutting down (^C received)')
    server.socket.close()

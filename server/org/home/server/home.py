from http.server import HTTPServer
import org.home.common.log as log
from org.home.server.request_handler import HomeRequestHandler
import signal
import threading

IP_ADDRESS = '0.0.0.0'
PORT_NUMBER = 8080


def shutdown_server(signal, frame):
    log.i('Shutting down (killed)')
    threading.Thread(daemon=True, target=server.shutdown).start()


log.init()
signal.signal(signal.SIGTERM, shutdown_server)

server = HTTPServer((IP_ADDRESS, PORT_NUMBER), HomeRequestHandler)
log.i('Started on port %s' % PORT_NUMBER)

try:
    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    log.i('Shutting down (^C received)')
    server.socket.close()

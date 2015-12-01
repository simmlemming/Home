from http.server import HTTPServer
import org.home.common.log as log
from org.home.server.request_handler import HomeRequestHandler

IP_ADDRESS = '0.0.0.0'
PORT_NUMBER = 8080

log.init()

server = HTTPServer((IP_ADDRESS, PORT_NUMBER), HomeRequestHandler)
log.i('Started on port %s' % PORT_NUMBER)

try:
    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    log.i('^C received, shutting down')
    server.socket.close()

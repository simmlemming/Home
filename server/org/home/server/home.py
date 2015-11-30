from http.server import HTTPServer

from org.home.server.request_handler import HomeRequestHandler

IP_ADDRESS = '127.0.0.1'
PORT_NUMBER = 8080

server = HTTPServer((IP_ADDRESS, PORT_NUMBER), HomeRequestHandler)
print('Started http server on port ', PORT_NUMBER)

try:
    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()

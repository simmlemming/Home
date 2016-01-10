import urllib.request as request
import urllib.error as error
import json
import time
from org.home.server.home import get_ip_from_args

SERVER_URL = 'http://{0}:8080/update'.format(get_ip_from_args())


def sensor_info(name, state):
    return {'name': name,
            'state': state}


def update(sensor_state):
    return {'time': int(time.time()),
            'state': 'on',
            'sensors': [
                sensor_info('Front door', sensor_state),
                sensor_info('Back door', 0),
                sensor_info('Kitchen door', 0),
                ]
            }

while True:
    print("\nServer: {0}".format(SERVER_URL))
    status = input("Enter status (0|1 or Empty line to read log): ")
    req = None

    if status == "":
        req = request.Request(SERVER_URL)
    else:
        dumped = json.dumps(update(status))  # String
        req = request.Request(SERVER_URL, dumped.encode('utf-8'))
        req.add_header('content-type', 'application/json')

    try:
        response = request.urlopen(req)
        content = response.read()
        print(content.decode('utf8'))

    except error.URLError as e:
        print("Cannot connect to server: " + str(e))

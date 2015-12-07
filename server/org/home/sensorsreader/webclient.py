import urllib.request as request
import urllib.error as error
import json
import time

SERVER_URL = 'http://80.240.140.181:8080/update'


def sensor_info(name, state):
    return {'name': name,
            'state': state}


def update(sensor_state):
    return {'time': time.time(),
            'state': 'on',
            'sensors': [
                sensor_info('Front door', sensor_state),
                sensor_info('Back door', 1),
                sensor_info('Kitchen door', 1),
                ]
            }

while True:
    status = input("\nEnter status (0|1 or Empty line to read log): ")
    req = None

    if status == "":
        req = request.Request(SERVER_URL)
    else:
        dumped = json.dumps(update(status))  # String
        req = request.Request(SERVER_URL, dumped.encode('ascii'))

    try:
        response = request.urlopen(req)
        content = response.read()
        print(content.decode('utf8'))

    except error.URLError as e:
        print("Cannot connect to server: " + str(e))

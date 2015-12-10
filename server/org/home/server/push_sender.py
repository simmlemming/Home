import org.home.server.storage as storage
import org.home.common.log as log
from org.home.server.config import PUSH_API_KEY
import urllib.request as http
import urllib.error
import json


def send_to_all(message):
    devices = storage.get_all_devices()

    if len(devices) == 0:
        log.i('No devices registered for push notifications')

    for name, token in devices:
        __send_to_one(name, token, message)


def __send_to_one(name, token, message):
    log.i('Sending {0} to {1}'.format(message, name))

    headers = {'Authorization': 'key=' + PUSH_API_KEY, 'Content-Type': 'application/json'}
    body = dict(to=token, data=dict(message=message))

    request = http.Request('https://gcm-http.googleapis.com/gcm/send',
                           json.dumps(body).encode('utf-8'), headers=headers)
    try:
        response = http.urlopen(request)
        content = response.read().decode('utf-8')

        content = json.loads(content)
        content = json.dumps(content, indent=4)
        log.i('Push notification sent to %s' % name)
        log.i(content)
    except urllib.error.HTTPError as e:
        error_message = e.read().decode('utf-8')

        log.e('Cannot send push notification to %s:' % name)
        log.e('\t%s %s' % (e.getcode(), e.reason))
        log.e('\t%s' % error_message)

if __name__ == "__main__":
    t = "eQ20SxLuBfo:APA91bG248G176XbWGWiIUaqUQSZo3O5vWEH5zOLZU8i-CFz29SQDtzvJv8wwrvpFBytlOz2l1HNXha_57AisUVWpbRntVfNyxBlWhicLnt8_5t7h0nN6yr1MxqTCuqbkzUNLU_OpJNH"
    __send_to_one("name", t, "abc sfjsifjwoifjwoiefj")

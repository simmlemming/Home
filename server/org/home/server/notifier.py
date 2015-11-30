import json


def notify_device_added(token):
    print("Device added")


def notify(cmp_result, update, sensors):
    message = "****** Notification ******\n\tCode: {0}\n\tSensors: {1}\n\tUpdate: {2}"
    print(message.format(cmp_result, json.dumps(sensors), json.dumps(update)))

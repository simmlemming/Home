import json
import org.home.common.log as log


def notify_device_added(token):
    log.i("Device added %s " % token)


def notify(cmp_result, update, sensors):
    message = "****** Notification ******\n\tCode: {0}\n\tSensors: {1}\n\tUpdate: {2}"
    log.i(message.format(cmp_result, json.dumps(sensors), json.dumps(update)))

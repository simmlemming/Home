import os
import time


def merge_sensors(sensors_1, sensors_2):
    merged = sensors_to_dict(sensors_1)
    s_2 = sensors_to_dict(sensors_2)

    for name in s_2:
        sensor = s_2[name]

        if name in merged:
            old_state = merged[name]['state']
            merged[name]['state'] = old_state | sensor['state']
        else:
            merged[sensor['name']] = sensor

    return list(merged.values())


def current_time_s():
    return int(time.time())


def validate_mode(mode):
    if 'mode' not in mode:
        return False

    return mode['mode'] in {'off', 'serve', 'guard'}


def validate_device(token):
    return ('device_token' in token) & ('device_name' in token)


def validate_update(update):
    all_fields_present = ('time' in update) & ('sensors' in update)

    if not all_fields_present:
        return False

    update_time = update['time']

    time_is_int = type(update_time) is int
    time_in_range = 1450656000 < update_time < 4604256000  # between 2016 and 2116

    return time_is_int & time_in_range


def rm(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        pass


def sensors_to_dict(sensors):
    d = {}
    for sensor in sensors:
        d[sensor['name']] = sensor
    return d
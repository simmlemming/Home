import os
import time


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

import os


def validate_device(token):
    return ('device_token' in token) & ('device_name' in token)


def validate_update(update):
    all_fields_present = ('state' in update) & ('time' in update) & ('sensors' in update)

    if not all_fields_present:
        return False

    time = update['time']

    time_is_int = type(time) is int
    time_in_range = 1450656000 < time < 4604256000  # between 2016 and 2116

    return time_is_int & time_in_range


def rm(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        pass

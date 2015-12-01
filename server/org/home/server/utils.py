def validate_device(token):
    return ('device_token' in token) & ('device_name' in token)


def validate_update(update):
    return ('state' in update) & ('time' in update) & ('sensors' in update)

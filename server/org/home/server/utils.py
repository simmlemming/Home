def validate_device(token):
    return token['token']


def validate_update(update):
    return ('state' in update) & ('time' in update) & ('sensors' in update)

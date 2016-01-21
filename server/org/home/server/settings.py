from org.home.server.storage import put, get_string

DEFAULT_MODE = 'off'


def put_mode(mode):
    put('mode', mode)


def get_mode():
    mode = get_string('mode', 'd')

    if mode == 'd':
        return DEFAULT_MODE

    return mode

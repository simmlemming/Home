import sqlite3
from sqlite3 import OperationalError
import json
import os.path

DATABASE_FILE_NAME = 'db.sqlite'
LAST_UPDATE_FILE_NAME = 'last_update.json'


class InvalidUpdate:
    pass


def get_db():
    db = sqlite3.connect(DATABASE_FILE_NAME)

    db.execute('create table if not exists log (t int, u text)')
    db.execute('create table if not exists devices (name text primary key, token text)')
    db.execute('create table if not exists settings (key text primary key, value text)')

    return db


def put(key, value):
    db = get_db()

    cursor = db.execute('insert or replace into settings values (?,?)', (key, value))
    added = cursor.rowcount == 1

    db.commit()
    db.close()

    if not added:
        raise OperationalError


def get_int(key, default_value):
    default_string_value = '--dv--'

    value = get_string(key, default_string_value)
    if value == default_string_value:
        return default_value

    return int(value)


def get_string(key, default_value):
    db = get_db()
    cursor = db.execute('select * from settings where key=?', (key,))
    fetched_tuple = cursor.fetchone()

    if not fetched_tuple:
        return default_value

    value = fetched_tuple[1]  # How to refer by column name?
    cursor.close()

    return value


def get_all_devices():
    db = get_db()

    cursor = db.execute('select name, token from devices')

    devices = cursor.fetchall()
    db.close()

    return devices


def add_device(token):
    db = get_db()

    cursor = db.execute('insert or replace into devices values (?,?)', (token['device_name'], token['device_token']))
    added = cursor.rowcount == 1

    db.commit()
    db.close()

    if not added:
        raise OperationalError


def save_last_update(update):
    with open(LAST_UPDATE_FILE_NAME, 'w') as file:
        file.write(json.dumps(update))


def get_last_update():
    if not os.path.isfile(LAST_UPDATE_FILE_NAME):
        return None

    with open(LAST_UPDATE_FILE_NAME, 'r') as file:
        last_update = file.read()
        return json.loads(last_update)


def add_to_log(update):
    db = get_db()

    cursor = db.execute('insert into log values(?,?)', (update['time'], json.dumps(update)))
    added = cursor.rowcount == 1;

    db.commit()
    db.close()

    if not added:
        raise OperationalError


def get_log():
    db = get_db()

    result = db.execute('select * from log')
    log = result.fetchall()

    db.close()
    return log

import sqlite3
import json
import os.path
import time

DATABASE_FILE_NAME = 'db.sqlite'
LAST_UPDATE_FILE_NAME = 'last_update.json'


class InvalidUpdate:
    pass


def add_device(token):
    db = sqlite3.connect(DATABASE_FILE_NAME)

    db.execute('create table if not exists devices (time real, token text)')
    db.execute('insert into devices values (?,?)', (time.time(), token['device_token']))

    db.commit()
    db.close()


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
    db = sqlite3.connect(DATABASE_FILE_NAME)
    __create_table(db)

    db.execute('insert into log values(?,?)', (update['time'], json.dumps(update)))

    db.commit()
    db.close()

    return 1  # cursor.rowcount


def get_log():
    db = sqlite3.connect(DATABASE_FILE_NAME)
    __create_table(db)

    result = db.execute('select * from log')
    all_statuses = result.fetchall()

    db.close()
    return all_statuses


def __create_table(db):
    db.execute('create table if not exists log (t real, u text)')

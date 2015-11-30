from sqlite3 import OperationalError

import org.home.server.notifier as notifier
from org.home.server.updates_comparator import Comparator

import org.home.server.storage as storage


def on_new_update(new_update):
    last_update = storage.get_last_update()

    if not last_update:
        storage.save_last_update(new_update)
        return

    result, sensors = Comparator().compare(last_update, new_update)

    if result != Comparator.RESULT_EQUALS:
        notifier.notify(result, new_update, sensors)
        saved_rows = storage.add_to_log(new_update)

        if saved_rows == 0:
            raise OperationalError

    else:
        print('No changes since last update')

    storage.save_last_update(new_update)

import org.home.server.notifier as notifier
import org.home.server.storage as storage
import org.home.common.log as log
from sqlite3 import OperationalError
from org.home.server.updates_comparator import Comparator
from org.home.server.utils import current_time_s
import org.home.server.settings as settings

MODE_OFF = 'off'
MODE_GUARD = 'guard'
MODE_SERVE = 'serve'

STATE_OK = 'ok'
STATE_ALARM = 'alarm'


def on_new_update(new_update):
    new_update['time'] = current_time_s()
    last_update = storage.get_last_update()
    storage.save_last_update(new_update)

    if not last_update:
        return

    result, sensors = Comparator().compare(last_update, new_update)

    if result != Comparator.RESULT_EQUALS:
        system_state = get_system_state()
        notifier.notify(result, system_state)
        saved_rows = storage.add_to_log(system_state)

        if saved_rows == 0:
            raise OperationalError

    else:
        log.d('No changes since last update')


def __state(sensors):
    for sensor in sensors:
        if sensor['state'] == 1:
            return STATE_ALARM

    return STATE_OK


def get_system_state():
    mode = settings.get_mode()

    if mode == MODE_OFF:
        return dict(mode=MODE_OFF, time=current_time_s())

    last_update = storage.get_last_update()
    if not last_update:
        last_update = dict(sensors=[])
        last_update['time'] = current_time_s()

    last_update['mode'] = settings.get_mode()
    last_update['state'] = __state(last_update['sensors'])
    return last_update
from org.home.server.utils import validate_update


def to_dict(sensors):
    d = {}
    for sensor in sensors:
        d[sensor['name']] = sensor
    return d


def check_for_new_sensors(old, new):
    old_sensors = to_dict(old)
    new_sensors = to_dict(new)
    added_sensors = []

    for sensor_name in new_sensors:
        if sensor_name not in old_sensors:
            added_sensors.append(new_sensors[sensor_name])

    if len(added_sensors) > 0:
        return added_sensors

    return None


def check_for_missing_sensors(old, new):
    old_sensors = to_dict(old)
    new_sensors = to_dict(new)
    removed_sensors = []

    for sensor_name in old_sensors:
        if sensor_name not in new_sensors:
            removed_sensors.append(old_sensors[sensor_name])

    if len(removed_sensors) > 0:
        return removed_sensors

    return None


def check_for_updated_sensors(old, new):
    old_sensors = to_dict(old)
    new_sensors = to_dict(new)
    updated_sensors = []

    for sensor_name, sensor in new_sensors.items():
        old_state = old_sensors[sensor_name]['state']
        if sensor['state'] != old_state:
            updated_sensors.append(sensor)

    return updated_sensors


class Comparator:
    RESULT_INTERNAL_ERROR = 1
    RESULT_EQUALS = 2
    RESULT_NEW_SENSOR = 3
    RESULT_MISSING_SENSOR = 4
    RESULT_SENSORS_UPDATED = 5
    RESULT_STATE_CHANGED = 6  # State of the system changed 'on' <-> 'off'

    # noinspection PyMethodMayBeStatic
    # returns code and list of sensors that changed
    def compare(self, old, new):
        if not old or not new:
            return Comparator.RESULT_INTERNAL_ERROR, None

        if not validate_update(old) or not validate_update(new):
            return Comparator.RESULT_INTERNAL_ERROR, None

        if old['state'] != new['state']:
            return Comparator.RESULT_STATE_CHANGED, None

        new_sensors = check_for_new_sensors(old['sensors'], new['sensors'])
        if new_sensors:
            return Comparator.RESULT_NEW_SENSOR, new_sensors

        missing_sensor = check_for_missing_sensors(old['sensors'], new['sensors'])
        if missing_sensor:
            return Comparator.RESULT_MISSING_SENSOR, missing_sensor

        updated_sensors = check_for_updated_sensors(old['sensors'], new['sensors'])
        if len(updated_sensors) != 0:
            return Comparator.RESULT_SENSORS_UPDATED, updated_sensors

        return Comparator.RESULT_EQUALS, None

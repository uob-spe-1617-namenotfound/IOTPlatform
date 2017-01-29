class User(object):
    def __init__(self, user_id, name, password_hash, email_address, is_admin):
        self.user_id = user_id
        self.name = name
        self.password_hash = password_hash
        self.email_address = email_address
        self.is_admin = is_admin

    def get_user_attributes(self):
        return {'user_id': self.user_id, 'name': self.name, 'password_hash': self.password_hash,
                'email_address': self.email_address, 'is_admin': self.is_admin}

    def get_user_id(self):
        return self.user_id


class House(object):
    def __init__(self, house_id, user_id, name):
        self.house_id = house_id
        self.user_id = user_id
        self.name = name

    def get_house_attributes(self):
        return {'house_id': self.house_id, 'user_id': self.user_id, 'name': self.name}

    @classmethod
    def from_dict(cls, d):
        h = House(user_id=d['user_id'] if 'user_id' in d else None,
                  house_id=d['_id'] if '_id' in d else None,
                  name=d['name'] if 'name' in d else "")
        return h


# House groups could be used for fleet management or for people with multiple houses
class HouseGroup(object):
    def __init__(self, house_group_id, house_ids, name):
        self.house_group_id = house_group_id
        self.house_ids = house_ids
        self.name = name

    def get_house_group_attributes(self):
        return {'house_group_id': self.house_group_id, 'house_ids': self.house_ids, 'name': self.name}


class Room(object):
    def __init__(self, room_id, house_id, name):
        self.room_id = room_id
        self.house_id = house_id
        self.name = name

    def get_room_attributes(self):
        return {'room_id': self.room_id, 'house_id': self.house_id, 'name': self.name}


# Room groups could be things like 'Upstairs', or to be used for templates
class RoomGroup(object):
    def __init__(self, room_group_id, room_ids, name):
        self.room_group_id = room_group_id
        self.room_ids = room_ids
        self.name = name

    def get_room_group_attributes(self):
        return {'room_group_id': self.room_group_id, 'room_ids': self.room_ids, 'name': self.name}


class Device(object):
    def __init__(self, device_id, house_id, room_id, name, device_type, power_state, last_read):
        self.device_id = device_id
        self.house_id = house_id
        self.room_id = room_id
        self.name = name
        self.device_type = device_type
        self.power_state = power_state
        self.last_read = last_read

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id,
                'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state,
                'last_read': self.last_read}

    def get_device_id(self):
        return self.device_id

    def get_device_type(self):
        return self.device_type


class Thermostat(Device):
    def __init__(self, device_id, house_id, room_id, name, power_state, last_read, last_temperature, target_temperature,
                 locked_max_temperature, locked_min_temperature, temperature_scale):
        Device.__init__(self, device_id, house_id, room_id, name, "thermostat", power_state, last_read)
        self.last_temperature = last_temperature
        self.target_temperature = target_temperature
        self.locked_max_temp = locked_max_temperature
        self.locked_min_temp = locked_min_temperature
        self.temperature_scale = temperature_scale

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id,
                'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state, 'last_read': self.last_read,
                'last_temperature': self.last_temperature, 'target_temperature': self.target_temperature,
                'locked_max_temp': self.locked_max_temp, 'locked_min_temp': self.locked_min_temp,
                'temperature_scale': self.temperature_scale}


class MotionSensor(Device):
    def __init__(self, device_id, house_id, room_id, name, power_state, last_read, sensor_data):
        Device.__init__(self, device_id, house_id, room_id, name, "motion_sensor", power_state, last_read)
        self.sensor_data = sensor_data

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id,
                'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state,
                'last_read': self.last_read, 'sensor_data': self.sensor_data}


class LightSwitch(Device):
    def __init__(self, device_id, house_id, room_id, name, power_state, last_read):
        Device.__init__(self, device_id, house_id, room_id, name, "light_switch", power_state, last_read)

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id,
                'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state,
                'last_read': self.last_read,}


class OpenSensor(Device):
    def __init__(self, device_id, house_id, room_id, name, power_state, last_read, sensor_data):
        Device.__init__(self, device_id, house_id, room_id, name, "open_sensor", power_state, last_read)
        self.sensor_data = sensor_data

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id,
                'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state,
                'last_read': self.last_read, 'sensor_data': self.sensor_data}


class DeviceGroup(object):
    def __init__(self, device_group_id, device_ids, name):
        self.device_group_id = device_group_id
        self.device_ids = device_ids
        self.name = name

    def get_device_group_attributes(self):
        return {'device_group_id': self.device_group_id, 'device_ids': self.device_ids, 'name': self.name}


class Trigger:
    def __init__(self, trigger, action):
        self.trigger_id = None
        self.trigger_sensor_id = None
        self.trigger = trigger
        self.actor_id = None
        self.action = action

    def get_trigger_attributes(self):
        return {'trigger_id': self.trigger_id, 'trigger_sensor_id': self.trigger_sensor_id,
                'trigger': self.trigger, 'actor_id': self.actor_id, 'action': self.action}

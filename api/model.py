class User(object):
    def __init__(self, name, password_hash, email_address, is_admin):
        self.user_id = None
        self.name = name
        self.password_hash = password_hash
        self.email_address = email_address
        self.is_admin = is_admin

    def get_user_attributes(self):
        return {'user_id': self.user_id, 'name': self.name, 'password_hash': self.password_hash,
                'email_address': self.email_address, 'is_admin': self.is_admin}

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id


class House(object):
    def __init__(self, name, user_id):
        self.user_id = user_id
        self.house_id = None
        self.name = name

    def get_house_attributes(self):
        return {'user_id': self.user_id, 'house_id': self.house_id, 'name': self.name}

    @classmethod
    def from_dict(cls, d):
        h = House(user_id=d['user_id'] if 'user_id' in d else None,
                  name=d['name'] if 'name' in d else "")
        h.set_house_id(str(d['_id']))
        return h

    def set_house_id(self, house_id):
        self.house_id = house_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

    def get_name(self):
        return self.name

    def get_house_id(self):
        return self.house_id


# House groups could be used for fleet management or for people with multiple houses
class HouseGroup(object):
    def __init__(self, name):
        self.house_group_id = None
        self.house_ids = []
        self.name = name

    def get_house_group_attributes(self):
        return {'house_group_id': self.house_group_id, 'house_ids': self.house_ids, 'name': self.name}

    def set_house_group_id(self, house_group_id):
        setattr(self, 'house_group_id', house_group_id)

    def add_house_to_group(self, house_id):
        self.house_ids.append(house_id)


class Room(object):
    def __init__(self, name, house_id):
        self.room_id = None
        self.house_id = house_id
        self.name = name

    def get_room_attributes(self):
        return {'room_id': self.room_id, 'house_id': self.house_id, 'name': self.name}

    def set_room_id(self, room_id):
        setattr(self, 'room_id', room_id)

    def set_house(self, house_id):
        setattr(self, 'house_id', house_id)


# Room groups could be things like 'Upstairs', or to be used for templates
class RoomGroup(object):
    def __init__(self, name):
        self.room_group_id = None
        self.room_ids = []
        self.name = name

    def get_room_group_attributes(self):
        return {'room_group_id': self.room_group_id, 'room_ids': self.room_ids, 'name': self.name}

    def set_room_group_id(self, room_group_id):
        setattr(self, 'room_group_id', room_group_id)

    def add_room_to_group(self, room_id):
        self.room_ids.append(room_id)


class Device:
    def __init__(self, name, device_type, power_state):
        self.house_id = None
        self.room_id = None
        self.device_id = None
        self.name = name
        self.device_type = device_type
        self.power_state = power_state

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id,
                'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state}

    def change_power_state(self):
        if self.power_state == 0:
            setattr(self, 'power_state', 1)
        else:
            setattr(self, 'power_state', 0)


class Thermostat(Device):
    def __init__(self):
        Device.__init__(self, name, "Thermostat", power_state)
        self.last_temperature = None
        self.target_temperature = None
        self.locked_max_temp = None
        self.locked_min_temp = None
        self.temperature_scale = "C"

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id,
                'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state,
                'last_temperature': self.last_temperature, 'target_temperature': self.target_temperature,
                'locked_max_temp': self.locked_max_temp, 'locked_min_temp': self.locked_min_temp,
                'temperature_scale': self.temperature_scale}

    def get_reading(self):
        return {'last_temperature': self.last_temperature}

    def change_temperature_scale(self):
        if self.temperature_scale == "C":
            setattr(self, 'temperature_scale', "F")
        else:
            setattr(self, 'temperature_scale', "C")


class MotionSensor(Device):
    def __init__(self):
        Device.__init__(self, name, "Motion Sensor", power_state)
        self.sensor_data = None

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id,
                'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state,
                'sensor_data': self.sensor_data}

    def get_reading(self):
        return {'sensor_data': self.sensor_data}


class PlugSocket(Device):
    def __init__(self):
        Device.__init__(self, name, "Plug Socket", power_state)

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id,
                'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state}


class OpenSensor(Device):
    def __init__(self):
        Device.__init__(self, name, "Door/Window Sensor", power_state)
        self.sensor_data = None

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id,
                'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state,
                'sensor_data': self.sensor_data}

    def get_reading(self):
        return {'sensor_data': self.sensor_data}


class DeviceGroup(object):
    def __init__(self, name):
        self.device_group_id = None
        self.device_ids = []
        self.name = name

    def get_device_group_attributes(self):
        return {'device_group_id': self.device_group_id, 'device_ids': self.device_ids, 'name': self.name}

    def set_device_group_id(self, device_group_id):
        setattr(self, 'device_group_id', device_group_id)

    def add_device_to_group(self, device_id):
        self.device_ids.append(device_id)


"""
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
"""

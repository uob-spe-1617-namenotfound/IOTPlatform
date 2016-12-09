import random
import string


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


def generate_id():
    return ''.join([random.choice(string.digits + string.ascii_lowercase) for _ in range(10)])


class UserRepository:
    def __init__(self):
        self.users = dict()

    def add_user(self, user):
        self.users[user.user_id] = user

    def remove_user(self, user_id):
        self.users.pop(user_id, None)

    def get_user_by_id(self, user_id):
        try:
            return self.users[user_id]
        except KeyError:
            print("User {} not found".format(user_id))


class House(object):
    def __init__(self, user_id, house_id, name):
        self.user_id = user_id
        self.house_id = house_id
        self.name = name

    def get_house_attributes(self):
        return {'user_id': self.user_id, 'house_id': self.house_id, 'name': self.name}


# House groups are for users with multiple houses, or for Fleet management
class HouseRepository:
    def __init__(self):
        self.houses = dict()

    def add_house(self, house):
        self.houses[house.house_id] = house

    def add_house_group(self, house_group):
        self.house_groups[house_group.id] = house_group
        self.house_groups.update({'id': house_group})

    def add_house_to_group(self, house_group):
        self.house_groups[house_group.id] += self.house_groups

    def remove_house(self, house_id):
        self.houses.pop(house_id, None)

    def get_house_by_id(self, house_id):
        try:
            return self.houses[house_id]
        except KeyError:
            print("House {} not found".format(house_id))

    def add_house_to_user(self, user_id, house_id):
        self.get_house_by_id(house_id).user_id = user_id

    def get_houses_for_user(self, user_id):
        return [house for house in self.houses.values() if house.user_id == user_id]

    def add_house_to_user(self, user, house):
        self.houses[house.user_id] = user.user_id
        house.user_id = user.user_id


class HouseGroup(object):
    def __init__(self, house_group_id, name):
        self.house_group_id = house_group_id
        self.house_ids = []
        self.name = name

    def get_house_group_attributes(self):
        return {'house_group_id': self.house_group_id, 'house_ids': self.house_ids, 'name': self.name}


class HouseGroupRepository:
    def __init__(self):
        self.house_groups = {}

    def add_house_group(self, house_group):
        self.house_groups[house_group.id] = house_group

    def add_house_to_group(self, house_group_id, house_id):
        self.get_house_group_by_id(house_group_id).house_ids.append(house_id)

    def get_house_group_by_id(self, house_group_id):
        if house_group_id in self.house_groups:
            return self.house_groups[house_group_id]
        return None

    def remove_house_group(self, house_group_id):
        self.house_groups.pop(house_group_id, None)


class Room(object):
    def __init__(self, room_id, house_id, name):
        self.house_id = house_id
        self.room_id = room_id
        self.name = name
        self.device_ids = []

    def get_room_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id, 'name': self.name, 'device_ids': self.device_ids}


# Room groups could be things like 'Upstairs', or to be used for templates
class RoomRepository:
    def __init__(self):
        self.rooms = dict()

    # TODO: add_room should generate an ID instead of accepting one (same for all other add_* functions)
    def add_room(self, room):
        self.rooms[room.room_id] = room

    def remove_room(self, room_id):
        return self.rooms.pop(room_id, None)

    def get_room_by_id(self, room_id):
        try:

            return self.rooms[room_id]
        except KeyError:
            print("Room {} not found".format(room_id))

    def add_room_to_house(self, house_id, room_id):
        self.rooms[room_id].house_id = house_id

    def get_rooms_for_house(self, house_id):
        return [room for room in self.rooms.values() if room.house_id == house_id]

    def add_device_to_room(self, room_id, device_id):
        self.get_room_by_id(room_id).device_ids.append(device_id)

    def generate_new_room_id(self):
        while True:
            key = generate_id()
            if key not in self.rooms:
                return key


class RoomGroup(object):
    def __init__(self, room_id, room_group_id, name):
        self.room_id = room_id
        self.room_group_id = room_group_id
        self.name = name

    def get_room_group_attributes(self):
        return {'room_id': self.room_id, 'room_group_id': self.room_group_id, 'name': self.name}


class RoomGroupRepository:
    def __init__(self):
        self.room_groups = {}

    def add_room_group(self, room_group):
        self.room_groups[room_group.room_group_id] = RoomGroup.get_room_group_attributes(room_group)

    def add_room_to_group(self, room_id, room_group):
        self.room_groups[room_group.id] += room_id

    def remove_room_group(self, room_group_id):
        self.room_groups.pop(room_group_id.id, None)

    def get_room_group_by_id(self, room_group_id):
        try:
            return self.room_groups[room_group_id]
        except KeyError:
            print("Room Group {} not found" % room_group_id)


class Device:
    def __init__(self, house_id, room_id, device_id, name, device_type, power_state, last_temp, target_temp,
                 sensor_data):
        self.house_id = house_id
        self.room_id = room_id
        self.device_id = device_id
        self.name = name

        self.device_type = device_type
        self.power_state = power_state
        self.last_temp = last_temp
        self.target_temp = target_temp
        self.sensor_data = sensor_data

    def get_device_attributes(self):
        return {'house_id': self.house_id, 'room_id': self.room_id, 'device_id': self.device_id, 'name': self.name,
                'device_type': self.device_type, 'power_state': self.power_state, 'last_temp': self.last_temp,
                'target_temp': self.target_temp, 'sensor_data': self.sensor_data}

    def change_power_state(self):
        try:
            if self.power_state == 1:
                self.power_state = 0
            elif self.power_state == 0:
                self.power_state = 1
        except:
            return "ERROR: Power State not 1 or 0"

    def set_target_temp(self, target):
        self.target_temp = target


class DeviceRepository:
    def __init__(self):
        self.devices = {}

    def add_device(self, device):
        self.devices[device.device_id] = device

    def add_new_device(self, device_type, house_id, name, access_data):
        device_id = self.generate_new_device_id()
        self.devices[device_id] = Device(house_id, None, device_id, name, device_type, 1, None, None, access_data)
        return self.get_device_by_id(device_id)

    def generate_new_device_id(self):
        while True:
            key = generate_id()
            if key not in self.devices:
                return key

    def remove_device(self, device_id):
        self.devices.pop(device_id, None)

    def get_device_by_id(self, device_id):
        try:
            return self.devices[device_id]
        except KeyError:
            print("Device {} not found".format(device_id))

    def add_device_to_house(self, house_id, device_id):
        self.get_device_by_id(device_id).house_id = house_id

    def get_devices_for_house(self, house_id):
        return [device for device in self.devices.values() if device.house_id == house_id]

    def get_devices_for_room(self, room_id):
        return [device for device in self.devices.values() if device.room_id == room_id]

    def link_device_to_room(self, room_id, device_id):
        device = self.get_device_by_id(device_id)
        device.room_id = room_id
        return device


class DeviceGroup(object):
    def __init__(self, device_group_id, device_ids, name):
        self.device_group_id = device_group_id
        self.device_ids = device_ids
        self.name = name

    def get_device_group_attributes(self):
        return {'device_ids': self.device_ids, 'device_group_id': self.device_group_id, 'name': self.name}


class DeviceGroupRepository:
    def __init__(self):
        self.device_groups = {}

    def add_device_group(self, device_group):
        self.device_groups[device_group.device_group_id] = device_group

    def add_device_to_group(self, device_id, device_group):
        self.device_groups[device_group.device_group_id].device_ids.append(device_id)

    def remove_device_group(self, device_group_id):
        self.device_groups.pop(device_group_id.device_group_id, None)

    def get_device_group_by_id(self, device_group_id):
        try:
            return self.device_groups[device_group_id]
        except KeyError:
            print("Device Group {} not found".format(device_group_id))


class Trigger:
    def __init__(self, trigger_id, trigger_sensor_id, trigger, actor_id, action):
        self.trigger_id = trigger_id
        self.trigger_sensor_id = trigger_sensor_id
        self.trigger = trigger
        self.actor_id = actor_id
        self.action = action

    def get_trigger_attributes(self):
        return {
            "trigger_id": self.trigger_id,
            "trigger_sensor_id": self.trigger_sensor_id,
            "trigger": self.trigger,
            "actor_id": self.actor_id,
            "action": self.action
        }


class TriggerRepository:
    def __init__(self):
        self.triggers = dict()

    def add_trigger(self, trigger_sensor_id, trigger, actor_id, action):
        # TODO: should check trigger_sensor_id and actor_id
        trigger_id = self.generate_new_trigger_id()
        self.triggers[trigger_id] = Trigger(trigger_id, trigger_sensor_id, trigger, actor_id, action)
        return self.get_trigger_by_id(trigger_id)

    def get_trigger_by_id(self, trigger_id):
        if trigger_id not in self.triggers:
            return None
        return self.triggers[trigger_id]

    def generate_new_trigger_id(self):
        while True:
            key = generate_id()
            if key not in self.triggers:
                return key

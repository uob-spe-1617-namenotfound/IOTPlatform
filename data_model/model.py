# import json


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


class UserRepository:
    def __init__(self):
        self.users = dict()

    def add_user(self, user):
        self.users[user.user_id] = User.get_user_attributes(user)

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
        self.houses[house.house_id] = House.get_house_attributes(house)


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
        return [house for house in self.houses if house.user_id == user_id]

    def add_house_to_user(self, user, house):
        self.houses[house.user_id] = user.user_id
        house.user_id = user.user_id

    def get_houses_for_user(self, user_id):
        lst = {}
        for house in self.houses:
            if house.user_id == user_id:
                lst += house
        return lst
        refs/remotes/benny/data_model


class HouseGroup(object):
    def __init__(self, house_group_id):
        self.house_group_id = house_group_id
        self.house_ids = []

    def get_house_group_attributes(self):
        return {'house_group_id': self.house_group_id, 'house_ids': self.house_ids}


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

    def add_room(self, room):
        self.rooms[room.room_id] = room

    def remove_room(self, room_id):
        self.rooms.pop(room_id, None)

    def get_room_by_id(self, room_id):
        try:

            return self.rooms[room_id]
        except KeyError:
            print("Room {} not found".format(room_id))

    def add_room_to_house(self, house_id, room_id):
        self.rooms[room_id].house_id = house_id

    def get_rooms_for_house(self, house_id):
        return [room for room in self.rooms if room.house_id == house_id]

    def add_device_to_room(self, room_id, device_id):
        self.get_room_by_id(room_id).device_ids.append(device_id)


class Device(object):
    def __init__(self, house_id, room_id, device_id, name, power_state):

class Device(Room):
    def __init__(self, house_id, room_id, device_id, name, device_type, power_state, last_temp, target_temp,
                 sensor_data):
        refs/remotes/benny/data_model
        self.house_id = house_id
        self.room_id = room_id
        self.device_id = device_id
        self.name = name


        self.device_type = device_type
        refs/remotes/benny/data_model
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
        return [device for device in self.devices if device.house_id == house_id]

def get_devices_for_room(self, devices, room_id):
    for device in devices:
        if device.room_id == room_id:
            return device

class DeviceGroup(object):
    def __init__(self, device_group_id, device_ids):
        self.device_group_id = device_group_id
        self.device_ids = device_ids


def get_device_group_attributes(self):
    return {'device_ids': self.device_ids, 'device_group_id': self.device_group_id}


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

            print("Device Group {} not found" % device_group_id)


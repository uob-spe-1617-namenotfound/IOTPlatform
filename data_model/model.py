import pymongo
from pymongo import MongoClient

# Connector to running database
mongo = MongoClient('localhost', 27017)
db = mongo.database

#Define database collections
users = db.users
houses = db.houses
house_groups = db.housegroups
rooms = db.rooms
room_groups = db.roomgroups


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

    def set_user_id(self, user_id):
        setattr(self, 'user_id', user_id)


class UserRepository():
    def add_user(self, user):
        new_user = User.get_user_attributes(user)
        name = new_user['name']
        password_hash = new_user['password_hash']
        email_address = new_user['email_address']
        is_admin = new_user['is_admin']
        user_id = users.insert_one({'name': name, 'password_hash': password_hash,
                                        'email_address': email_address, 'is_admin': is_admin})
        User.set_user_id(user, user_id)

    def remove_user(self, user_id):
        users.delete_one({'_id': user_id})

    def get_user_by_id(self, user_id):
        user = users.find_one_or_404({'_id': user_id})
        target_user = User(user['Name'], user['password_hash'],
                           user['email_address'], user['is_admin'])
        User.set_user_id(target_user, user_id)
        return target_user


class House(object):
    def __init__(self, name):
        self.user_id = None
        self.house_id = None
        self.name = name

    def get_house_attributes(self):
        return {'user_id': self.user_id, 'house_id': self.house_id, 'name': self.name}

    def set_house_id(self, house_id):
        setattr(self, 'house_id', house_id)

    def set_user(self, user_id):
        setattr(self, 'user_id', user_id)


class HouseRepository:
    def add_house(self, house):
        new_house = House.get_house_attributes(house)
        name = new_house['name']
        house_id = houses.insert_one({'name': name})
        House.set_house_id(house, house_id)

    def remove_house(self, house_id):
        houses.delete_one({'_id': house_id})

    def get_house_by_id(self, house_id):
        house = houses.find_one_or_404({'_id': house_id})
        name = house['name']
        target_house = House(name)
        House.set_house_id(target_house, house_id)
        House.set_user(target_house, house['user_id'])
        return target_house

    def add_house_to_user(self, user, house):
        target_house = House.get_house_attributes(house)
        target_user = User.get_user_attributes(user)
        house_id = target_house['house_id']
        user_id = target_user['user_id']
        House.set_user(house, user_id)
        houses.update({'_id': house_id}, {"$set": {'user_id': user_id}}, upsert = False)

    def get_houses_for_user(self, user_id):
        return houses.find({'user_id': user_id})


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


class HouseGroupRepository:
    def add_house_group(self, house_group):
        new_house_group = HouseGroup.get_house_group_attributes(house_group)
        house_ids = new_house_group['house_ids']
        name = new_house_group['name']
        house_group_id = house_groups.insert_one({'house_ids': house_ids, 'name': name})
        HouseGroup.set_house_group_id(house_group, house_group_id)


    def add_house_to_group(self, house_group, house):
        target_house = House.get_house_attributes(house)
        target_house_group = HouseGroup.get_house_group_attributes(house_group)
        house_id = target_house['house_id']
        house_group_id = target_house_group['house_group_id']
        house_groups.update({'_id': house_group_id}, {"$push": {'house_ids': house_id}}, upsert = False)

    def remove_house_group(self, house_group_id):
        house_groups.delete_one({'_id': house_group_id})


class Room(object):
    def __init__(self, name):
        self.room_id = None
        self.house_id = None
        self.name = name

    def get_room_attributes(self):
        return {'room_id': self.room_id, 'house_id': self.house_id, 'name': self.name}

    def set_room_id(self, room_id):
        setattr(self, 'room_id', room_id)

    def set_house(self, house_id):
        setattr(self, 'house_id', house_id)


class RoomRepository:
    def add_room(self, room):
        new_room = Room.get_room_attributes(room)
        name = new_room['name']
        room_id = rooms.insert_one({'name': name})
        Room.set_room_id(room, room_id)

    def remove_room(self, room_id):
        rooms.delete_one({'_id': room_id})

    def get_room_by_id(self, room_id):
        room = rooms.find_one_or_404({'_id': room_id})
        target_room = Room(room['name'])
        Room.set_room_id(target_room, room_id)
        Room.set_house(target_room, room['house_id'])
        return target_room

    def add_room_to_house(self, house, room):
        target_room = Room.get_room_attributes(room)
        target_house = House.get_house_attributes(house)
        room_id = target_room['room_id']
        house_id = target_house['house_id']
        Room.set_house(room, house_id)
        rooms.update({'_id': room_id}, {"$set": {'house_id': house_id}}, upsert = False)

    def get_rooms_for_house(self, house_id):
        return rooms.find({'house_id': house_id})


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


class RoomGroupRepository:
    def add_room_group(self, room_group):
        new_room_group = RoomGroup.get_room_group_attributes(room_group)
        room_ids = new_room_group['room_ids']
        name = new_room_group['name']
        room_group_id = room_groups.insert({'room_ids': room_ids, 'name': name})
        RoomGroup.set_room_group_id(room_group, room_group_id)

    def add_room_to_group(self, room_group, room):
        target_room = Room.get_room_attributes(room)
        target_room_group = RoomGroup.get_room_group_attributes(room_group)
        room_id = target_room['room_id']
        room_group_id = target_room_group['room_group_id']
        room_groups.update({'_id': room_group_id}, {"$push": {'room)ids': room_id}}, upsert = False)

    def remove_room_group(self, room_group_id):
        room_groups.delete_one({'_id': room_group_id})

    def get_room_group_by_id(self, room_group_id):
        room_group = room_groups.find_one_or_404({'_id': room_group_id})
        target_room_group = RoomGroup(room_group['name'])
        RoomGroup.set_room_group_id(target_room_group, room_group_id)
        rooms = room_group['room_ids']
        for room_id in rooms:
            RoomGroup.add_room_to_group(target_room_group, room_id)
        return target_room_group


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


class DeviceRepository:
    #def add_device(self, device):

    def add_new_device(self, device_type, house_id, name, access_data):

    def remove_device(self, device_id):

    def get_device_by_id(self, device_id):

    def add_device_to_house(self, house_id, device_id):

    def get_devices_for_house(self, house_id):

    def get_devices_for_room(self, room_id):

    def link_device_to_room(self, room_id, device_id):


class DeviceGroup(object):
    def __init__(self, name):
        self.device_group_id = None
        self.device_ids = []
        self.name = name

    def get_device_group_attributes(self):
        return {'device_group_id': self.device_group_id, 'device_ids': self.device_ids, 'name': self.name}

class DeviceGroupRepository:
    def __init__(self):
        self.device_groups = db.devicegroups

    def add_device_group(self, device_group):

    def add_device_to_group(self, device_id, device_group):

    def remove_device_group(self, device_group_id):

    def get_device_group_by_id(self, device_group_id):

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

class TriggerRepository:
    def _init_(self):
        self.triggers = db.triggers

    def add_trigger(self, trigger_sensor_id, trigger, actor_id, action):

    def get_trigger_by_id(self, trigger_id):

    def generate_new_trigger_id(self): """

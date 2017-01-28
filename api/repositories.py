import logging

from model import HouseGroup, House, Room, RoomGroup, User, Device, DeviceGroup, Thermostat, MotionSensor, PlugSocket, OpenSensor


class Repository(object):
    def __init__(self, mongo_collection):
        self.collection = mongo_collection

    def clear_db(self):
        self.collection.delete_many({})


class UserRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_user(self, name, password_hash, email_address, is_admin):
        user = self.collection.insert_one({'name': name, 'password_hash': password_hash,
                                           'email_address': email_address, 'is_admin': is_admin})
        return user.inserted_id

    def remove_user(self, user_id):
        self.collection.delete_one({'_id': user_id})

    def get_user_by_id(self, user_id):
        user = self.collection.find_one_or_404({'_id': user_id})
        target_user = User(user['user_id'], user['Name'],
                           user['password_hash'], user['email_address'],
                           user['is_admin'])
        return target_user

    def get_all_users(self):
        return self.collection.find()


class HouseRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_house(self, user_id, name):
        house = self.collection.insert_one({'user_id': user_id, 'name': name})
        return house.inserted_id

    def remove_house(self, house_id):
        self.collection.delete_one({'_id': house_id})

    def get_house_by_id(self, house_id):
        house = self.collection.find_one_or_404({'_id': house_id})
        target_house = House(house['house_id'], house['user_id'], house['name'])
        return target_house

    def get_houses_for_user(self, user_id):
        all_houses = self.collection.find({})
        logging.debug("Found {} houses".format(all_houses.count()))
        for h in all_houses:
            logging.debug("house: {}".format(h))
        return [House.from_dict(h) for h in self.collection.find({'user_id': user_id})]


class HouseGroupRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_house_group(self, house_ids, name):
        house_group = self.collection.insert_one({'house_ids': house_ids, 'name': name})
        return house_group.inserted_id

    def add_house_to_group(self, house_group_id, house_id):
        self.collection.update({'_id': house_group_id}, {"$push": {'house_ids': house_id}}, upsert=False)

    def remove_house_group(self, house_group_id):
        self.collection.delete_one({'_id': house_group_id})


class RoomRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_room(self, house_id, name):
        room = self.collection.insert_one({'house_id': house_id, 'name': name})
        return room.inserted_id

    def remove_room(self, room_id):
        self.collection.delete_one({'_id': room_id})

    def get_room_by_id(self, room_id):
        room = self.collection.find_one_or_404({'_id': room_id})
        target_room = room(room['room_id'], room['house_id'], room['name'])
        return target_room

    def get_rooms_for_house(self, house_id):
        return self.collection.find({'house_id': house_id})


class RoomGroupRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_room_group(self, room_group):
        new_room_group = room_group.get_room_group_attributes()
        room_ids = new_room_group['room_ids']
        name = new_room_group['name']
        room_group_id = self.collection.insert({'room_ids': room_ids, 'name': name})
        room_group.set_room_group_id(room_group_id)

    def add_room_to_group(self, room_group, room):
        target_room = Room.get_room_attributes(room)
        target_room_group = room_group.get_room_group_attributes()
        room_id = target_room['room_id']
        room_group_id = target_room_group['room_group_id']
        self.collection.update({'_id': room_group_id}, {"$push": {'room)ids': room_id}}, upsert=False)

    def remove_room_group(self, room_group_id):
        self.collection.delete_one({'_id': room_group_id})

    def get_room_group_by_id(self, room_group_id):
        room_group = self.collection.find_one_or_404({'_id': room_group_id})
        target_room_group = RoomGroup(room_group['name'])
        target_room_group.set_room_group_id(room_group_id)
        rooms = room_group['room_ids']
        for room_id in rooms:
            target_room_group.add_room_to_group(room_id)
        return target_room_group


class DeviceRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_device(self, house_id, room_id, name, device_type, power_state):
        device = self.collection.insert_one({'house_id': house_id, 'room_id': room_id,
                                                'name': name, 'device_type': device_type,
                                                'power_state': power_state})
        return device.inserted_id

    def remove_device(self, device_id):
        self.collection.delete_one({'_id': device_id})

    def get_device_by_id(self, device_id):
        device = self.collection.find_one_or_404({'_id': device_id})
        if device['device_type'] == "Thermostat":
            target_device = Thermostat(device['device_id'], device['house_id'], device['room_id'], device['name'],
                                       device['power_state'], device['locked_max_temperature'],
                                       device['locked_min_temperature'], device['temperature_scale'])
            target_device.last_temperature = device['last_temperature']
            target_device.last_read = device['last_read']
        elif device['device_type'] == "Motion Sensor":
            target_device = MotionSensor(device['device_id'], device['house_id'], device['room_id'], device['name'],
                                       device['power_state'])
            target_device.last_read = device['last_read']
            target_device.sensor_data = device['sensor_data']
        elif device['device_type'] == "Plug Socket":
            target_device = PlugSocket(device['device_id'], device['house_id'], device['room_id'], device['name'],
                                       device['power_state'])
            target_device.last_read = device['last_read']
        elif device['device_type'] == "Open Sensor":
            target_device = OpenSensor(device['device_id'], device['house_id'], device['room_id'], device['name'],
                                       device['power_state'])
            target_device.last_read = device['last_read']
            target_device.sensor_data = device['sensor_data']
        return target_device

    def add_device_to_house(self, house_id, device_id):
        self.collection.update({'_id': device_id}, {"$set": {'house_id': house_id}}, upsert = False)

    def get_devices_for_house(self, house_id):
        return self.collection.find({'house_id': house_id})

    def link_device_to_room(self, room_id, device_id):
        self.collection.update({'_id': device_id}, {"$set": {'room_id': room_id}}, upsert = False)

    def get_devices_for_room(self, room_id):
        return self.collection.find({'room_id': room_id})

    def set_target_temperature(self, device_id, temp):
        device = self.collection.find_one_or_404({'_id': device_id})
        assert (device['device_type'] == "Thermostat"), "Device is not a thermostat."
        assert (device['locked_min_temp'] <= temp), "Chosen temperature is too low."
        assert (device['locked_max_temp'] >= temp), "Chosen temperature is too high."
        self.collection.update({'_id': device_id}, {"$set": {'target_temperature': temp}}, upsert=False)

    def change_temperature_scale(self, device_id):
        device = self.collection.find_one_or_404({'_id': device_id})
        assert (device['device_type'] == "Thermostat"), "Device is not a thermostat."
        if device['temperature_scale'] == "C":
            self.collection.update({'_id': device_id}, {"$set": {'temperature_scale': "F"}}, upsert=False)
            new_target_temperature = device['target_temperature'] * 9/5 + 32
            new_max_temperature = device['locked_max_temp'] * 9/5 + 32
            new_min_temperature = device['locked_min_temp'] * 9/5 + 32
            new_last_temperature = device['last_temperature'] * 9/5 + 32
        else:
            self.collection.update({'_id': device_id}, {"$set": {'temperature_scale': "C"}}, upsert=False)
            new_target_temperature = (device['target_temperature'] - 32) * 5/9
            new_max_temperature = (device['locked_max_temp'] - 32) * 5/9
            new_min_temperature = (device['locked_min_temp'] - 32) * 5/9
            new_last_temperature = (device['last_temperature'] - 32) * 5/9
        self.collection.update({'_id': device_id}, {"$set": {'target_temperature': new_target_temperature}}, upsert=False)
        self.collection.update({'_id': device_id}, {"$set": {'locked_max_temp': new_max_temperature}}, upsert=False)
        self.collection.update({'_id': device_id}, {"$set": {'locked_min_temp': new_min_temperature}}, upsert=False)
        self.collection.update({'_id': device_id}, {"$set": {'last_temperature': new_last_temperature}}, upsert=False)


class DeviceGroupRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_device_group(self, device_group):
        new_device_group = device_group.get_device_group_attributes()
        device_ids = new_device_group['device_ids']
        name = new_device_group['name']
        device_group_id = self.collection.insert_one({'device_ids': device_ids, 'name': name})
        device_group.set_device_group_id(device_group_id)

    def add_device_to_group(self, device_id, device_group):
        pass

    def remove_device_group(self, device_group_id):
        pass

    def get_device_group_by_id(self, device_group_id):
        pass


class TriggerRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_trigger(self, trigger_sensor_id, trigger, actor_id, action):
        pass

    def get_trigger_by_id(self, trigger_id):
        pass

    def generate_new_trigger_id(self):
        pass

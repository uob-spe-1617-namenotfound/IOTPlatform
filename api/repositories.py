import logging

from model import HouseGroup, House, Room, RoomGroup, User, Device, DeviceGroup, Thermostat, MotionSensor, LightSwitch, \
    OpenSensor


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
        user = self.collection.find_one({'_id': user_id})
        target_user = User(user['_id'], user['name'],
                           user['password_hash'], user['email_address'],
                           user['is_admin'])
        return target_user

    def get_all_users(self):
        users = self.collection.find()
        target_users = []
        for user in users:
            target_users.append(User(user['_id'], user['name'], user['password_hash'], user['email_address'],
                                     user['is_admin']))
        return target_users


class HouseRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_house(self, user_id, name):
        house = self.collection.insert_one({'user_id': user_id, 'name': name})
        return house.inserted_id

    def remove_house(self, house_id):
        self.collection.delete_one({'_id': house_id})

    def get_house_by_id(self, house_id):
        house = self.collection.find_one({'_id': house_id})
        target_house = House(house['_id'], house['user_id'], house['name'])
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

    def remove_house_from_group(self, house_group_id, house_id):
        self.collection.update({'_id': house_group_id}, {"$pull": {'device_ids': house_id}}, upsert=False)

    def get_house_group_by_id(self, house_group_id):
        house_group = self.collection.find_one({'_id': house_group_id})
        target_house_group = HouseGroup(house_group['house_group_id'], house_group['house_ids'], house_group['name'])
        return target_house_group


class RoomRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_room(self, house_id, name):
        room = self.collection.insert_one({'house_id': house_id, 'name': name})
        return room.inserted_id

    def remove_room(self, room_id):
        self.collection.delete_one({'_id': room_id})

    def get_room_by_id(self, room_id):
        room = self.collection.find_one({'_id': room_id})
        target_room = Room(room['_id'], room['house_id'], room['name'])
        return target_room

    def get_rooms_for_house(self, house_id):
        rooms = self.collection.find({'house_id': house_id})
        target_rooms = []
        for room in rooms:
            target_rooms.append(Room(room['_id'], house_id, room['name']))
        return target_rooms


class RoomGroupRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_room_group(self, room_ids, name):
        room_group = self.collection.insert_one({'room_ids': room_ids, 'name': name})
        return room_group.inserted_id

    def add_room_to_group(self, room_group_id, room_id):
        self.collection.update({'_id': room_group_id}, {"$push": {'room_ids': room_id}}, upsert=False)

    def remove_room_group(self, room_group_id):
        self.collection.delete_one({'_id': room_group_id})

    def remove_room_from_group(self, room_group_id, room_id):
        self.collection.update({'_id': room_group_id}, {"$pull": {'device_ids': room_id}}, upsert=False)

    def get_room_group_by_id(self, room_group_id):
        room_group = self.collection.find_one({'_id': room_group_id})
        target_room_group = RoomGroup(room_group['room_group_id'], room_group['room_ids'], room_group['name'])
        return target_room_group


class DeviceRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def get_faulty_devices(self):
        all_device_ids = [x['_id'] for x in self.collection.find({}, {})]
        devices = []
        for device_id in all_device_ids:
            device = self.get_device_by_id(device_id)
            if device.is_faulty():
                devices.append(device)
        return devices


    def update_device_reading(self, device):
        reading = device.read_current_state()
        logging.debug("Read current state of device {}: {}".format(device.get_device_id(), reading))
        self.collection.update({'_id': device.get_device_id()},
                               {"$set": {"last_read": reading}})

    def update_all_device_readings(self):
        all_device_ids = [x['_id'] for x in self.collection.find({}, {})]
        for device_id in all_device_ids:
            device = self.get_device_by_id(device_id)
            self.update_device_reading(device)

    def add_device(self, house_id, room_id, name, device_type, power_state, configuration, vendor):
        device = self.collection.insert_one({'house_id': house_id, 'room_id': room_id,
                                             'name': name, 'device_type': device_type,
                                             'power_state': power_state,
                                             'configuration': configuration,
                                             'vendor': vendor})
        device_id = device.inserted_id
        self.collection.update({'_id': device_id}, {"$set": {'last_read': 0}})
        # self.set_device_type(device_id)
        device = self.get_device_by_id(device_id=device_id)
        self.update_device_reading(device)
        return device

    def set_device_type(self, device_id):
        device = self.collection.find_one({'_id': device_id})
        if device['device_type'] == "thermostat":
            self.collection.update({'_id': device_id}, {"$set": {'locked_max_temperature': 50}})
            self.collection.update({'_id': device_id}, {"$set": {'locked_min_temperature': 0}})
            self.collection.update({'_id': device_id}, {"$set": {'temperature_scale': "C"}})
            self.collection.update({'_id': device_id}, {"$set": {'target_temperature': 25}})
            self.collection.update({'_id': device_id}, {"$set": {'last_temperature': 0}})
        elif device['device_type'] == "motion_sensor":
            self.collection.update({'_id': device_id}, {"$set": {'sensor_data': 0}})
        # elif device['device_type'] == "light_switch":
        elif device['device_type'] == "open_sensor":
            self.collection.update({'_id': device_id}, {"$set": {'sensor_data': 0}})

    def remove_device(self, device_id):
        self.collection.delete_one({'_id': device_id})

    def get_device_by_id(self, device_id):
        device = self.collection.find_one({'_id': device_id})
        if device is None:
            return None
        device_type = device['device_type'] if 'device_type' in device else None
        if device_type == "thermostat":
            return Thermostat(device)
        elif device_type == "motion_sensor":
            return MotionSensor(device)
        elif device_type == "light_switch":
            return LightSwitch(device)
        elif device_type == "open_sensor":
            return OpenSensor(device)
        return Device(device)

    def add_device_to_house(self, house_id, device_id):
        self.collection.update({'_id': device_id}, {"$set": {'house_id': house_id}}, upsert=False)

    def get_devices_for_house(self, house_id):
        devices = self.collection.find({'house_id': house_id})
        target_devices = []
        for device in devices:
            target_devices.append(Device(device))
        return target_devices

    def link_device_to_room(self, room_id, device_id):
        self.collection.update({'_id': device_id}, {"$set": {'room_id': room_id}}, upsert=False)
        return self.get_device_by_id(device_id)

    def get_devices_for_room(self, room_id):
        devices = self.collection.find({'room_id': room_id})
        target_devices = []
        for device in devices:
            target_devices.append(Device(device))
        return target_devices
    def set_power_state(self, device_id, power_state):
        device = self.get_device_by_id(device_id)
        assert(device.device_type == "light_switch"), "Device is not a switch."
        device.configure_power_state(power_state)
        self.update_device_reading(device)
        return device


    def set_target_temperature(self, device_id, temp):
        device = self.collection.find_one({'_id': device_id})
        assert (device['device_type'] == "thermostat"), "Device is not a thermostat."
        assert ('locked_min_temperature' not in device or device[
            'locked_min_temperature'] <= temp), "Chosen temperature is too low."
        assert ('locked_max_temperature' not in device or device[
            'locked_max_temperature'] >= temp), "Chosen temperature is too high."
        self.collection.update({'_id': device_id}, {"$set": {'target_temperature': temp}}, upsert=False)
        device = self.get_device_by_id(device_id)
        device.configure_target_temperature(temp)
        self.update_device_reading(device)
        return device

    def change_temperature_scale(self, device_id):
        device = self.collection.find_one({'_id': device_id})
        assert (device['device_type'] == "thermostat"), "Device is not a thermostat."
        if device['temperature_scale'] == "C":
            self.collection.update({'_id': device_id}, {"$set": {'temperature_scale': "F"}}, upsert=False)
            new_target_temperature = device['target_temperature'] * 9 / 5 + 32
            new_max_temperature = device['locked_max_temp'] * 9 / 5 + 32
            new_min_temperature = device['locked_min_temp'] * 9 / 5 + 32
            new_last_temperature = device['last_temperature'] * 9 / 5 + 32
        else:
            self.collection.update({'_id': device_id}, {"$set": {'temperature_scale': "C"}}, upsert=False)
            new_target_temperature = (device['target_temperature'] - 32) * 5 / 9
            new_max_temperature = (device['locked_max_temp'] - 32) * 5 / 9
            new_min_temperature = (device['locked_min_temp'] - 32) * 5 / 9
            new_last_temperature = (device['last_temperature'] - 32) * 5 / 9
        self.collection.update({'_id': device_id}, {"$set": {'target_temperature': new_target_temperature}},
                               upsert=False)
        self.collection.update({'_id': device_id}, {"$set": {'locked_max_temp': new_max_temperature}}, upsert=False)
        self.collection.update({'_id': device_id}, {"$set": {'locked_min_temp': new_min_temperature}}, upsert=False)
        self.collection.update({'_id': device_id}, {"$set": {'last_temperature': new_last_temperature}}, upsert=False)


class DeviceGroupRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_device_group(self, device_ids, name):
        device_group = self.collection.insert_one({'device_ids': device_ids, 'name': name})
        return device_group.inserted_id

    def add_device_to_group(self, device_group_id, device_id):
        self.collection.update({'_id': device_group_id}, {"$push": {'device_ids': device_id}}, upsert=False)

    def remove_device_group(self, device_group_id):
        self.collection.delete_one({'_id': device_group_id})

    def remove_device_from_group(self, device_group_id, device_id):
        self.collection.update({'_id': device_group_id}, {"$pull": {'device_ids': device_id}}, upsert=False)

    def get_device_group_by_id(self, device_group_id):
        device_group = self.collection.find_one({'_id': device_group_id})
        target_device_group = DeviceGroup(device_group['device_group_id'], device_group['device_ids'],
                                          device_group['name'])
        return target_device_group


class TriggerRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_trigger(self, trigger_sensor_id, trigger, actor_id, action):
        pass

    def get_trigger_by_id(self, trigger_id):
        pass

    def generate_new_trigger_id(self):
        pass

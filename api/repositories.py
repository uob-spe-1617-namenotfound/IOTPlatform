import logging

from model import HouseGroup, House, Room, RoomGroup, User, Device, DeviceGroup


class Repository(object):
    def __init__(self, mongo_collection):
        self.collection = mongo_collection

    def clear_db(self):
        self.collection.delete_many({})


class HouseGroupRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_house_group(self, house_group):
        new_house_group = house_group.get_house_group_attributes()
        house_ids = new_house_group['house_ids']
        name = new_house_group['name']
        result = self.collection.insert_one({'house_ids': house_ids, 'name': name})
        house_group_id = result.inserted_id
        house_group.set_house_group_id(house_group_id)

    def add_house_to_group(self, house_group, house):
        target_house = house.get_house_attributes()
        target_house_group = house_group.get_house_group_attributes()
        house_id = target_house['house_id']
        house_group_id = target_house_group['house_group_id']
        self.collection.update({'_id': house_group_id}, {"$push": {'house_ids': house_id}}, upsert=False)

    def remove_house_group(self, house_group_id):
        self.collection.delete_one({'_id': house_group_id})


class RoomRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_room(self, room):
        new_room = room.get_room_attributes()
        name = new_room['name']
        result = self.collection.insert_one({'name': name})
        room_id = result.inserted_id
        room.set_room_id(room_id)

    def remove_room(self, room_id):
        self.collection.delete_one({'_id': room_id})

    def get_room_by_id(self, room_id):
        room = self.collection.find_one_or_404({'_id': room_id})
        target_room = room(room['name'])
        target_room.set_room_id(room_id)
        target_room.set_house(room['house_id'])
        return target_room

    def add_room_to_house(self, house, room):
        target_room = room.get_room_attributes()
        target_house = house.get_house_attributes()
        room_id = target_room['room_id']
        house_id = target_house['house_id']
        room.set_house(house_id)
        self.collection.update({'_id': room_id}, {"$set": {'house_id': house_id}}, upsert=False)

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

    def add_device(self, device):
        new_device = device.get_device_attributes()
        name = new_device['name']
        device_type = new_device['device_type']
        power_state = new_device['power_state']
        device_id = self.collection.insert_one({'name': name, 'device_type': device_type,
                                        'power_state': power_state})
        device.set_device_id(device_id)

    #def add_new_device(self, device_type, house_id, name, access_data):

    def remove_device(self, device_id):
        self.collection.delete_one({'_id': device_id})

    def get_device_by_id(self, device_id):
        device = self.collection.find_one_or_404({'_id': device_id})
        target_device = Device(device['name'], device['device_type'], device['power_state'])
        target_device.set_device_id(device_id)
        target_device.set_house(device['house_id'])
        target_device.set_room(device['room_id'])
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


class UserRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_user(self, user):
        new_user = User.get_user_attributes(user)
        name = new_user['name']
        password_hash = new_user['password_hash']
        email_address = new_user['email_address']
        is_admin = new_user['is_admin']
        result = self.collection.insert_one({'name': name, 'password_hash': password_hash,
                                             'email_address': email_address, 'is_admin': is_admin})
        user_id = result.inserted_id
        user.set_user_id(user_id)

    def remove_user(self, user_id):
        self.collection.delete_one({'_id': user_id})

    def get_user_by_id(self, user_id):
        user = self.collection.find_one_or_404({'_id': user_id})
        target_user = User(user['Name'], user['password_hash'],
                           user['email_address'], user['is_admin'])
        target_user.set_user_id(user_id)
        return target_user


class HouseRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_house(self, house):
        result = self.collection.insert_one({'name': house.get_name(), 'user_id': house.get_user_id()})
        house_id = result.inserted_id
        house.set_house_id(house_id)

    def remove_house(self, house_id):
        self.collection.delete_one({'_id': house_id})

    def get_house_by_id(self, house_id):
        house = self.collection.find_one_or_404({'_id': house_id})
        name = house['name']
        target_house = House(name)
        target_house.set_house_id(house_id)
        target_house.set_user(house['user_id'])
        return target_house

    def add_house_to_user(self, user, house):
        target_house = House.get_house_attributes(house)
        target_user = User.get_user_attributes(user)
        house_id = target_house['house_id']
        user_id = target_user['user_id']
        house.set_user(user_id)
        self.collection.update({'_id': house_id}, {"$set": {'user_id': user_id}}, upsert=False)

    def get_houses_for_user(self, user_id):
        all_houses = self.collection.find({})
        logging.debug("Found {} houses".format(all_houses.count()))
        for h in all_houses:
            logging.debug("house: {}".format(h))
        return [House.from_dict(h) for h in self.collection.find({'user_id': user_id})]


class TriggerRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_trigger(self, trigger_sensor_id, trigger, actor_id, action):
        pass

    def get_trigger_by_id(self, trigger_id):
        pass

    def generate_new_trigger_id(self):
        pass

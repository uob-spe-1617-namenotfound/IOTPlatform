import logging

from model import HouseGroup, House, Room, RoomGroup, User


class Repository(object):
    def __init__(self, mongo_collection):
        self.collection = mongo_collection


class HouseGroupRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_house_group(self, house_group):
        new_house_group = HouseGroup.get_house_group_attributes(house_group)
        house_ids = new_house_group['house_ids']
        name = new_house_group['name']
        result = self.collection.insert_one({'house_ids': house_ids, 'name': name})
        house_group_id = result.inserted_id
        HouseGroup.set_house_group_id(house_group, house_group_id)

    def add_house_to_group(self, house_group, house):
        target_house = House.get_house_attributes(house)
        target_house_group = HouseGroup.get_house_group_attributes(house_group)
        house_id = target_house['house_id']
        house_group_id = target_house_group['house_group_id']
        self.collection.update({'_id': house_group_id}, {"$push": {'house_ids': house_id}}, upsert=False)

    def remove_house_group(self, house_group_id):
        self.collection.delete_one({'_id': house_group_id})


class RoomRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_room(self, room):
        new_room = Room.get_room_attributes(room)
        name = new_room['name']
        result = self.collection.insert_one({'name': name})
        room_id = result.inserted_id
        Room.set_room_id(room, room_id)

    def remove_room(self, room_id):
        self.collection.delete_one({'_id': room_id})

    def get_room_by_id(self, room_id):
        room = self.collection.find_one_or_404({'_id': room_id})
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
        self.collection.update({'_id': room_id}, {"$set": {'house_id': house_id}}, upsert=False)

    def get_rooms_for_house(self, house_id):
        return self.collection.find({'house_id': house_id})


class RoomGroupRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_room_group(self, room_group):
        new_room_group = RoomGroup.get_room_group_attributes(room_group)
        room_ids = new_room_group['room_ids']
        name = new_room_group['name']
        room_group_id = self.collection.insert({'room_ids': room_ids, 'name': name})
        RoomGroup.set_room_group_id(room_group, room_group_id)

    def add_room_to_group(self, room_group, room):
        target_room = Room.get_room_attributes(room)
        target_room_group = RoomGroup.get_room_group_attributes(room_group)
        room_id = target_room['room_id']
        room_group_id = target_room_group['room_group_id']
        self.collection.update({'_id': room_group_id}, {"$push": {'room)ids': room_id}}, upsert=False)

    def remove_room_group(self, room_group_id):
        self.collection.delete_one({'_id': room_group_id})

    def get_room_group_by_id(self, room_group_id):
        room_group = self.collection.find_one_or_404({'_id': room_group_id})
        target_room_group = RoomGroup(room_group['name'])
        RoomGroup.set_room_group_id(target_room_group, room_group_id)
        rooms = room_group['room_ids']
        for room_id in rooms:
            RoomGroup.add_room_to_group(target_room_group, room_id)
        return target_room_group


class DeviceRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    # def add_device(self, device):

    def add_new_device(self, device_type, house_id, name, access_data):
        pass

    def remove_device(self, device_id):
        pass

    def get_device_by_id(self, device_id):
        pass

    def add_device_to_house(self, house_id, device_id):
        pass

    def get_devices_for_house(self, house_id):
        pass

    def get_devices_for_room(self, room_id):
        pass

    def link_device_to_room(self, room_id, device_id):
        pass


class DeviceGroupRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_device_group(self, device_group):
        pass

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
        User.set_user_id(user, user_id)

    def remove_user(self, user_id):
        self.collection.delete_one({'_id': user_id})

    def get_user_by_id(self, user_id):
        user = self.collection.find_one_or_404({'_id': user_id})
        target_user = User(user['Name'], user['password_hash'],
                           user['email_address'], user['is_admin'])
        User.set_user_id(target_user, user_id)
        return target_user


class HouseRepository(Repository):
    def __init__(self, mongo_collection):
        Repository.__init__(self, mongo_collection)

    def add_house(self, house):
        logging.debug("adding house: {}".format(house.get_house_attributes()))
        result = self.collection.insert_one({'name': house.get_name(), 'user_id': house.get_user_id()})
        house_id = result.inserted_id
        house.set_house_id(house_id)

    def remove_house(self, house_id):
        self.collection.delete_one({'_id': house_id})

    def get_house_by_id(self, house_id):
        house = self.collection.find_one_or_404({'_id': house_id})
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

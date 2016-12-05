class User(object):
    def __init__(self, user_id, name, password_hash, email_address, is_admin):
        self.user_id        = user_id
        self.name           = name
        self.password_hash  = password_hash
        self.email_address  = email_address
        self.is_admin       = is_admin

class UserRepository:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.id] = user

    def extend_repo(self, *users):
        for user in users:
            self.add(user)

    def remove_user(self, user):
        self.users.pop(user.id, None)

    def get_user_by_id(self, user_id):
        try:
            return self.users[user_id]
        except KeyError:
            print("User %d not found" % user_id)

    def add_house_to_user(self, user, house):
        self.users[user.id] = []
        self.users[user.id] += HouseRepository.users[user.id]

    def get_houses_for_user(self, user):
        return self.users[user.id]



class House(User):
    def __init__(self, user_id, house_id, name):
        self.user_id  = user_id
        self.house_id = house_id
        self.name     = name

# House groups are for users with multiple houses, or for Fleet management
class HouseRepository:
    def __init__(self):
        self.houses       = {}
        self.house_groups = {}

    def add_house(self, house):
        self.houses[house.id] = house

    def add_house_group(self, house_group):
        self.house_groups[house_group.id] = house_group

    def add_house_to_group(self, house, house_group):
        # If this method is called multiple times for a specific group, would the first line reset the group to []?
        self.house_groups[house_group.id] = []
        self.house_groups[house_group.id] += self.house_groups[house.id]

    def extend_repo(self, *houses):
        for house in houses:
            self.add(house)

    def remove_house(self, house):
        self.houses.pop(house.id, None)

    def remove_house_group(self, house_group):
        self.house_groups.pop(house_group.id, None)

    def get_house_by_id(self, house_id):
        try:
            return self.houses[house_id]
        except KeyError:
            print("House %d not found" % house_id)

    def add_room_to_house(self, house, room):
        self.houses[house.id] = []
        self.houses[house.id] += RoomRepository.rooms[room.id]

    def add_device_to_house(self, house, device):
        self.houses[house.id] = []
        self.houses[house.id] += DeviceRepository.devices[device.id]

    def get_devices_for_house(self, house):
        devs = []
        for elem in self.houses[house.id]:
            if elem in DeviceRepository.devices:
                devs += elem
        return devs

    def get_rooms_for_house(self, house):
        room = []
        for elem in self.houses[house.id]:
            if elem in RoomRepository.rooms:
                room += []
        return room



class Room(House):
    def __init__(self, house_id, room_id, name):
        self.house_id = house_id
        self.room_id  = room_id
        self.name     = name

# Room groups could be things like 'Upstairs', or to be used for templates
class RoomRepository:
    def __init__(self):
        self.rooms       = {}
        self.room_groups = {}

    def add_room(self, room):
        self.rooms[room.id] = room

    def add_room_group(self, room_group):
        self.room_groups[room_group.id] = room_group

    def add_room_to_group(self, room, room_group):
        self.room_groups[room_group.id] = []
        self.room_groups[room_group.id] += self.rooms[room.id]

    def extend_repo(self, *rooms):
        for room in rooms:
            self.add(room)

    def remove_room(self, room):
        self.rooms.pop(room.id, None)

    def get_room_by_id(self, room_id):
        try:
            return self.rooms[room_id]
        except KeyError:
            print("Room %d not found" % room_id)

    def add_device_to_room(self, room, device):
        self.rooms[room.id] = []
        self.rooms[room.id] += DeviceRepository.devices[device.id]

    def get_devices_for_room(self, room):
        return self.rooms[room.id]



class Device(House, Room):
    def __init__(self, house_id, room_id, device_id, name, power_state):
        self.house_id     = house_id
        self.room_id      = room_id
        self.device_id    = device_id
        self.name         = name
        self.power_state  = power_state

    def change_power_state(self):
        try:
            if self.power_state == 1:
                power_state = 0
            elif self.power_state == 0:
                power_state = 1
        except:
            return "ERROR: Power State not 1 or 0"

class DeviceRepository:
    def __init__(self):
        self.devices       = {}
        self.device_groups = {}

    def add_device_to_devices(self, device):
        self.devices[device.id] = device

    def add_device_group(self, device_group):
        self.device_groups[device_group.id] = device_group

    def add_device_to_group(self, device, device_group):
        self.device_groups[device_group.id] = []
        self.device_groups[device_group.id] += self.devices[device.id]

    def extend_device_repo(self, *devices):
        for device in devices:
            self.add(device)

    def remove_device(self, device):
        self.devices.pop(device.id, None)

    def remove_device_group(self, device_group):
        self.device_groups.pop(device_group.id, None)

    def get_device_by_id(self, device_id):
        try:
            return self.devices[device_id]
        except KeyError:
            print("Device %d not found" % device_id)

    def get_device_group_by_id(self, device_group_id):
        try:
            return self.device_groups[device_group_id]
        except KeyError:
            print("Device Group %d not found" % device_group_id)
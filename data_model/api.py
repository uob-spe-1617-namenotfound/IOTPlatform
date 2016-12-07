from flask import Flask, jsonify

from data_model import model

api = Flask("SPE-IoT-API")
api.config.from_pyfile('data_model/config.cfg')

user_repository = model.UserRepository()
user1 = model.User("user_id_1", "Jack Xia", "xxxxxxxx", "nobody@gmail.com", False)
user_repository.add_user(user1)
house_repository = model.HouseRepository()
house1 = model.House("user_id_1","house_id_1","Jack's house")
house_repository.add_house(house1)
room_repository = model.RoomRepository()
room1 = model.Room("house_id_1","Room_id_1", "Kitchen")
room_repository.add_room(room1)
room2 = model.Room("house_id_1","Room_id_2", "Bathroom")
room_repository.add_room(room2)
room3 = model.Room("house_id_1","Room_id_3", "Living Room")
room_repository.add_room(room3)
device_repository = model.DeviceRepository()
device1 = model.Device("house_id_1","'room_id_1", "device_id_1", "Theromstat", "on")
device_repository.add_device(device1)
devicegroup_repository = model.DeviceGroupRepository()
devicegroup = model.DeviceGroups("devicegroup_id_1")
devicegroup_repository.add_device_group(devicegroup)
@api.route('/user/<string:user_id>')
def get_user_info(user_id):
    user = user_repository.get_user_by_id(user_id)
    return jsonify({"user": user.get_user_attributes(), "error": None})

@api.route('/house/<string:house_id>')
def get_house_info(house_id):
    house = house_repository.get_house_by_id(house_id)
    return jsonify({"house": house.get_house_attributes(), "error": None})

@api.route('/house/<string:room_id>')
def get_room_info(room_id):
    room = room_repository.get_room_by_id(room_id)
    return jsonify({"room":room.get_room_attributes(), "errors": None})

@api.route('/device/<string:device_id>')
def get_device_info(device_id):
    device = device_repository.get_device_by_id(device_id)
    return jsonify({"device":device.get_device_attributes(), "errors": None})

@api.route('/devicegroup/<string:devicegroup_id>')
def get_devicegroup_info(devicegroup_id):
    devicegroup = devicegroup_repository.get_devicegroup_by_id(devicegroup_id)
    return jsonify({"devicegroup":devicegroup.get_devicegroup_attributes(), "errors": None})

@api.route('/device/<string:device_id>')
def remove_device(device_id):
    device = device_repository.remove_devices_for_house(device_id)
    return jsonify({"device":device.remove_device_attributes(),"errors": None})

@api.route('/device/<string:device_id>')
def add_device(device_id):
    device = device_repository.get_devices_for_house(device_id)
    return jsonify({"device":device.get_device_attributes(),"errors": None})

def main():
    api.run(debug=True, host=api.config['HOSTNAME'], port=int(api.config['PORT']))

if __name__ == "__main__":
    main()


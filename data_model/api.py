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
room1 = model.Room("room_id_1","house_id_1", "Kitchen")
room_repository.add_room(room1)
room2 = model.Room("room_id_2","house_id_1", "Bathroom")
room_repository.add_room(room2)
room3 = model.Room("room_id_3","house_id_1", "Living Room")
room_repository.add_room(room3)
device_repository = model.DeviceRepository()
device1 = model.Device("house_id_1","'room_id_1", "device_id_1", "Theromstat", "on")
device_repository.add_device(device1)
devicegroup_repository = model.DeviceGroupRepository()
devicegroup = model.DeviceGroup("devicegroup_id_1",[])
devicegroup_repository.add_device_group(devicegroup)
@api.route('/user/<string:user_id>')
def get_user_info(user_id):
    user = user_repository.get_user_by_id(user_id)
    if user is None:
        return jsonify({"user": None, "error": {"code":404, "messaage": "No such user found"}})
    return jsonify({"user": user.get_user_attributes(), "error": None})

@api.route('/house/<string:house_id>')
def get_house_info(house_id):
    house = house_repository.get_house_by_id(house_id)
    if house is None:
        return jsonify({"house": None, "error": {"code":404, "messaage": "No such house found"}})
    return jsonify({"house": house.get_house_attributes(), "error": None})

@api.route('/room/<string:room_id>')
def get_room_info(room_id):
    room = room_repository.get_room_by_id(room_id)
    if room is None:
        return jsonify({"room": None, "error": {"code":404, "messaage": "No such room found"}})
    return jsonify({"room":room.get_room_attributes(), "errors": None})

@api.route('/device/<string:device_id>')
def get_device_info(device_id):
    device = device_repository.get_device_by_id(device_id)
    if device is None:
        return jsonify({"user": None, "error": {"code":404, "messaage": "No such device found"}})
    return jsonify({"device":device.get_device_attributes(), "errors": None})

@api.route('/devicegroup/<string:devicegroup_id>')
def get_devicegroup_info(devicegroup_id):
    devicegroup = devicegroup_repository.get_devicegroup_by_id(devicegroup_id)
    if devicegroup is None:
        return jsonify({"user": None, "error": {"code":404, "messaage": "No such devicegroup found"}})
    return jsonify({"devicegroup":devicegroup.get_devicegroup_attributes(), "errors": None})

@api.route('/device/<string:device_id>/add',methods = ['POST'])
def add_device(device):
    device = model.Device("whatever house id exists", "a room id", device, "name of the device", 0)
    device_repository.add_device(device)
    #device = device_repository.get_devices_for_house(device_id)
    return jsonify({"a device has been added")

@api.route('/device/<string:device_id>/remove',methods = ['POST'])
def remove_device(device_id):
    device = model.Device("whatever house id exists", "a room id", device_id, "name of the device", 0)
    device_repository.remove_device(device_id)
    #device = device_repository.remove_devices_for_house(device_id)
    if device is None:
        return jsonify({"user": None, "error": {"code": 404, "messaage": "No such device found"}})
    return jsonify({"device":device.remove_device_attributes(),"errors": None})

@api.route('/room/<string:room_id>/add',methods = ['POST'])
def add_room(room):
    room = model.Room(room, "house_id", "name of the room")
    room_repository.add_room(room)
    return jsonify("a room has been added")

@api.route('/device/<string:device_id>/remove',methods = ['POST'])
def remove_room(room_id):
    room = model.Room(room_id, "a house id",  "name of the room")
    device_repository.remove_room(room_id)
    #device = device_repository.remove_devices_for_house(device_id)
    if room is None:
        return jsonify({"user": None, "error": {"code": 404, "messaage": "No such device found"}})
    return jsonify({"device":room.remove_room_attributes(),"errors": None})



def main():
    api.run(debug=True, host=api.config['HOSTNAME'], port=int(api.config['PORT']))

if __name__ == "__main__":
    main()


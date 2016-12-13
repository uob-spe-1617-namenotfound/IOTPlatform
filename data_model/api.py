from flask import Flask, jsonify, request

from data_model import model

# TODO: better error handling
api = Flask("SPE-IoT-API")
api.config.from_pyfile('data_model/config.cfg')

user_repository = model.UserRepository()
user1 = model.User("user_id_1", "Jack Xia", "xxxxxxxx", "nobody@gmail.com", False)
user_repository.add_user(user1)
house_repository = model.HouseRepository()
house1 = model.House("user_id_1", "house_id_1", "Jack's house")
house_repository.add_house(house1)
room_repository = model.RoomRepository()
room1 = model.Room("room_id_1", "house_id_1", "Kitchen")
room_repository.add_room(room1)
room2 = model.Room("room_id_2", "house_id_1", "Bathroom")
room_repository.add_room(room2)
room3 = model.Room("room_id_3", "house_id_1", "Living Room")
room_repository.add_room(room3)
device_repository = model.DeviceRepository()
device1 = model.Device("device_id_1", "house_id_1", "room_id_1", "Bedroom thermostat", "thermostat",
                       {"url": "http://localhost:5010/thermostat/1"}, vendor="OWN")
device_repository.add_device(device1)
device2 = model.Device("device_id_2", "house_id_1", None, "Backyard motion sensor", "motion_sensor",
                       {"url": "http://localhost:5010/motion_sensor/2"}, vendor="OWN")
device_repository.add_device(device2)
device3 = model.Device("device_id_3", "house_id_1", None, "Backyard motion sensor", "motion_sensor",
                       {"url": "http://localhost:5010/motion_sensor/2"}, vendor="OWN")
device_repository.add_device(device3)
devicegroup_repository = model.DeviceGroupRepository()
devicegroup = model.DeviceGroup("devicegroup_id_1", [], "Group 1")
devicegroup_repository.add_device_group(devicegroup)

trigger_repository = model.TriggerRepository()


@api.route('/user/<string:user_id>')
def get_user_info(user_id):
    user = user_repository.get_user_by_id(user_id)
    if user is None:
        return jsonify({"user": None, "error": {"code": 404, "message": "No such user found"}})
    return jsonify({"user": user.get_user_attributes(), "error": None})


@api.route('/users')
def get_all_users():
    users = user_repository.get_all_users()
    return jsonify({"users": [user.get_user_attributes() for user in users], "error": None})


@api.route('/user/<string:user_id>/houses')
def get_houses_for_user(user_id):
    houses = house_repository.get_houses_for_user(user_id)
    if houses is None:
        return jsonify({"houses": None, "error": {"code": 404, "message": "No such user found"}})
    return jsonify({"houses": [house.get_house_attributes() for house in houses], "error": None})


@api.route('/house/<string:house_id>')
def get_house_info(house_id):
    house = house_repository.get_house_by_id(house_id)
    if house is None:
        return jsonify({"house": None, "error": {"code": 404, "message": "No such house found"}})
    return jsonify({"house": house.get_house_attributes(), "error": None})


@api.route('/room/<string:room_id>')
def get_room_info(room_id):
    room = room_repository.get_room_by_id(room_id)
    if room is None:
        return jsonify({"room": None, "error": {"code": 404, "message": "No such room found"}})
    return jsonify({"room": room.get_room_attributes(), "error": None})


@api.route('/house/<string:house_id>/rooms')
def get_rooms_for_house(house_id):
    rooms = room_repository.get_rooms_for_house(house_id)
    if rooms is None:
        return jsonify({"rooms": None, "error": {"code": 404, "message": "No such house found"}})
    return jsonify({"rooms": [room.get_room_attributes() for room in rooms], "error": None})


@api.route('/room/<string:room_id>/devices')
def get_devices_for_room(room_id):
    devices = device_repository.get_devices_for_room(room_id)
    if devices is None:
        return jsonify({"devices": None, "error": {"code": 404, "message": "No such room found"}})
    return jsonify({"devices": [device.get_device_attributes() for device in devices], "error": None})


@api.route('/house/<string:house_id>/devices')
def get_devices_for_house(house_id):
    devices = device_repository.get_devices_for_house(house_id)
    if devices is None:
        return jsonify({"devices": None, "error": {"code": 404, "message": "No such house found"}})
    return jsonify({"devices": [device.get_device_attributes() for device in devices], "error": None})


@api.route('/device/<string:device_id>')
def get_device_info(device_id):
    device = device_repository.get_device_by_id(device_id)
    if device is None:
        return jsonify({"user": None, "error": {"code": 404, "message": "No such device found"}})
    return jsonify({"device": device.get_device_attributes(), "error": None})


@api.route('/devicegroup/<string:device_group_id>')
def get_devicegroup_info(device_group_id):
    device_group = devicegroup_repository.get_device_group_by_id(device_group_id)
    if device_group is None:
        return jsonify({"device_group": None, "error": {"code": 404, "message": "No such device group found"}})
    return jsonify({"device_group": device_group.get_devicegroup_attributes(), "errors": None})


@api.route('/house/<string:house_id>/devices/add', methods=['POST'])
def add_device(house_id):
    print(request.get_json())
    data = request.get_json()
    device = device_repository.add_new_device(data['device_type'], house_id, data['name'], data['configuration'],
                                              data['vendor'])
    if device is None:
        return jsonify({"device": None, "error": {"code": 400, "message": "Device could not be added"}})
    return jsonify({"device": device.get_device_attributes(), "error": None})


@api.route('/device/<string:device_id>/remove', methods=['POST'])
def remove_device(device_id):
    result = device_repository.remove_device(device_id)
    if result is None:
        return jsonify({"device_id": None, "error": {"code": 404, "message": "No such device found"}})
    return jsonify({"device_id": result.device_id, "error": None})


@api.route('/house/<string:house_id>/rooms/add', methods=['POST'])
def add_room(house_id):
    data = request.get_json()
    room_id = room_repository.generate_new_room_id()
    room = model.Room(room_id, house_id, data['name'])
    room_repository.add_room(room)
    room = room_repository.get_room_by_id(room_id)
    return jsonify({"room": room.get_room_attributes(), "error": None})


@api.route('/room/<string:room_id>/device/<string:device_id>/link')
def link_device_to_room(room_id, device_id):
    result = device_repository.link_device_to_room(room_id, device_id)
    if result is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such device found."}})
    return jsonify({"device": result.get_device_attributes(), "error": None})


@api.route('/device/<string:device_id>/triggers/add', methods=['POST'])
def add_trigger(device_id):
    data = request.get_json()
    trigger = data['trigger']
    actor_id = data['actor_id']
    action = data['action']
    result = trigger_repository.add_trigger(device_id, trigger, actor_id, action)
    if result is None:
        return jsonify({"trigger": None, "error": {"code": 404, "message": "Trigger couldn't be created."}})
    return jsonify({"trigger": result.get_trigger_attributes(), "error": None})


@api.route('/device/<string:device_id>/thermostat/configure', methods=['POST'])
def configure_thermostat(device_id):
    data = request.get_json()
    target_temperature = data['target_temperature']
    device = device_repository.get_device_by_id(device_id)
    device.set_target_temp(target_temperature)
    return jsonify({
        "device": device.get_device_attributes(),
        "error": None
    })


def main():
    api.run(debug=True, host=api.config['HOSTNAME'], port=int(api.config['PORT']))


if __name__ == "__main__":
    main()

import json
import logging

from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient

from cron import setup_cron

# TODO: better error handling
api = Flask("SPE-IoT-API")
api.config.from_pyfile('config.cfg')
logging.basicConfig(level=logging.DEBUG)
# Connector to running database
mongo = MongoClient(api.config['MONGO_HOST'], api.config['MONGO_PORT'])
db = mongo.database
authentication = api.config['AUTHENTICATION_ENABLED']


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


api.json_encoder = JSONEncoder

import repositories

api.repository_collection = repositories.RepositoryCollection(db)

api.user_repository = api.repository_collection.user_repository
api.house_repository = api.repository_collection.house_repository
api.room_repository = api.repository_collection.room_repository
api.device_repository = api.repository_collection.device_repository
api.devicegroup_repository = api.repository_collection.devicegroup_repository
api.trigger_repository = api.repository_collection.trigger_repository
api.token_repository = api.repository_collection.token_repository


@api.route('/login')
def login():
    pass


@api.route('/logout')
def logout():
    pass


@api.route('/user/default_user')
def get_first_user_id():
    users = api.user_repository.get_all_users()
    first_user = users[0]
    user_id = first_user.get_user_id()
    return jsonify({"user_id": user_id})


@api.route('/user/<string:user_id>')
def get_user_info(user_id, token):
    access = api.token_repository.authenticate_user(ObjectId(user_id), token)
    if access is False:
        return jsonify({"user": None, "error": {"code": 401, "message": "Authentication failed"}})
    user = api.user_repository.get_user_by_id(ObjectId(user_id))
    if user is None:
        return jsonify({"user": None, "error": {"code": 404, "message": "No such user found"}})
    return jsonify({"user": user.get_user_attributes(), "error": None})


@api.route('/users')
def get_all_users():
    users = api.user_repository.get_all_users()
    return jsonify({"users": [user.get_user_attributes() for user in users], "error": None})


@api.route('/user/<string:user_id>/houses')
def get_houses_for_user(user_id, token):
    access = api.token_repository.authenticate_user(ObjectId(user_id), token)
    if access is False:
        return jsonify({"houses": None, "error": {"code": 401, "message": "Authentication failed"}})
    logging.debug("Getting houses for user {}".format(user_id))
    houses = api.house_repository.get_houses_for_user(ObjectId(user_id))
    if houses is None:
        return jsonify({"houses": None, "error": {"code": 404, "message": "No such user found"}})
    return jsonify({"houses": [house.get_house_attributes() for house in houses], "error": None})


@api.route('/house/<string:house_id>')
def get_house_info(house_id, token):
    access = api.house_repository.validate_token(ObjectId(house_id), token)
    if access is False:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    house = api.house_repository.get_house_by_id(ObjectId(house_id))
    if house is None:
        return jsonify({"house": None, "error": {"code": 404, "message": "No such house found"}})
    return jsonify({"house": house.get_house_attributes(), "error": None})


@api.route('/room/<string:room_id>')
def get_room_info(room_id, token):
    access = api.room_repository.validate_token(ObjectId(room_id), token)
    if access is False:
        return jsonify({"room": None, "error": {"code": 401, "message": "Authentication failed"}})
    room = api.room_repository.get_room_by_id(ObjectId(room_id))
    if room is None:
        return jsonify({"room": None, "error": {"code": 404, "message": "No such room found"}})
    return jsonify({"room": room.get_room_attributes(), "error": None})


@api.route('/house/<string:house_id>/rooms')
def get_rooms_for_house(house_id, token):
    access = api.house_repository.validate_token(ObjectId(house_id), token)
    if access is False:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    rooms = api.room_repository.get_rooms_for_house(ObjectId(house_id))
    if rooms is None:
        return jsonify({"rooms": None, "error": {"code": 404, "message": "No such house found"}})
    return jsonify({"rooms": [room.get_room_attributes() for room in rooms], "error": None})


@api.route('/room/<string:room_id>/devices')
def get_devices_for_room(room_id, token):
    access = api.room_repository.validate_token(ObjectId(room_id), token)
    if access is False:
        return jsonify({"room": None, "error": {"code": 401, "message": "Authentication failed"}})
    devices = api.device_repository.get_devices_for_room(ObjectId(room_id))
    if devices is None:
        return jsonify({"devices": None, "error": {"code": 404, "message": "No such room found"}})
    return jsonify({"devices": [device.get_device_attributes() for device in devices], "error": None})


@api.route('/house/<string:house_id>/devices')
def get_devices_for_house(house_id, token):
    access = api.house_repository.validate_token(ObjectId(house_id), token)
    if access is False:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    devices = api.device_repository.get_devices_for_house(ObjectId(house_id))
    if devices is None:
        return jsonify({"devices": None, "error": {"code": 404, "message": "No such house found"}})
    return jsonify({"devices": [device.get_device_attributes() for device in devices], "error": None})


@api.route('/device/<string:device_id>')
def get_device_info(device_id, token):
    access = api.device_repository.validate_token(ObjectId(device_id), token)
    if access is False:
        return jsonify({"device": None, "error": {"code": 401, "message": "Authentication failed"}})
    device = api.device_repository.get_device_by_id(ObjectId(device_id))
    if device is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such device found"}})
    return jsonify({"device": device.get_device_attributes(), "error": None})


@api.route('/devicegroup/<string:device_group_id>')
def get_devicegroup_info(device_group_id):
    device_group = api.devicegroup_repository.get_device_group_by_id(ObjectId(device_group_id))
    if device_group is None:
        return jsonify({"device_group": None, "error": {"code": 404, "message": "No such device group found"}})
    return jsonify({"device_group": device_group.get_devicegroup_attributes(), "errors": None})


@api.route('/house/<string:house_id>/devices/add', methods=['POST'])
def add_device(house_id, token):
    access = api.house_repository.validate_token(ObjectId(house_id), token)
    if access is False:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    data = request.get_json()
    logging.debug("Adding device: {}".format(data))
    device = api.device_repository.add_device(device_type=data['device_type'],
                                              house_id=ObjectId(house_id),
                                              room_id=None,
                                              name=data['name'],
                                              power_state=None,
                                              configuration=data['configuration'],
                                              vendor=data['vendor'])
    logging.debug("Device added: {}".format(device))
    if device is None:
        return jsonify({"device": None, "error": {"code": 400, "message": "Device could not be added"}})
    return jsonify({"device": device.get_device_attributes(), "error": None})


@api.route('/device/<string:device_id>/remove', methods=['POST'])
def remove_device(device_id, token):
    access = api.device_repository.validate_token(ObjectId(device_id), token)
    if access is False:
        return jsonify({"device_id": None, "error": {"code": 401, "message": "Authentication failed"}})
    result = api.device_repository.remove_device(ObjectId(device_id))
    if result is None:
        return jsonify({"device_id": None, "error": {"code": 404, "message": "No such device found"}})
    return jsonify({"device_id": result.device_id, "error": None})


@api.route('/house/<string:house_id>/rooms/add', methods=['POST'])
def add_room(house_id, token):
    access = api.house_repository.validate_token(ObjectId(house_id), token)
    if access is False:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    data = request.get_json()
    room_id = api.room_repository.add_room(ObjectId(house_id), data['name'])
    room = api.room_repository.get_room_by_id(room_id)
    return jsonify({"room": room.get_room_attributes(), "error": None})


@api.route('/room/<string:room_id>/device/<string:device_id>/link')
def link_device_to_room(room_id, device_id, token):
    access1 = api.room_repository.validate_token(ObjectId(room_id), token)
    access2 = api.device_repository.validate_token(ObjectId(device_id), token)
    if access1 is False or access2 is False:
        return jsonify({"room": None, "error": {"code": 401, "message": "Authentication failed"}})
    result = api.device_repository.link_device_to_room(ObjectId(room_id), ObjectId(device_id))
    if result is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such device found."}})
    return jsonify({"device": result.get_device_attributes(), "error": None})


@api.route('/device/<string:device_id>/triggers/add', methods=['POST'])
def add_trigger(device_id, token):
    access = api.device_repository.validate_token(ObjectId(device_id), token)
    if access is False:
        return jsonify({"device": None, "error": {"code": 401, "message": "Authentication failed"}})
    data = request.get_json()
    trigger = data['trigger']
    actor_id = data['actor_id']
    action = data['action']
    result = api.trigger_repository.add_trigger(ObjectId(device_id), trigger, ObjectId(actor_id), action)
    if result is None:
        return jsonify({"trigger": None, "error": {"code": 404, "message": "Trigger couldn't be created."}})
    return jsonify({"trigger": result.get_trigger_attributes(), "error": None})


@api.route('/device/<string:device_id>/thermostat/configure', methods=['POST'])
def configure_thermostat(device_id, token):
    access = api.device_repository.validate_token(ObjectId(device_id), token)
    if access is False:
        return jsonify({"device": None, "error": {"code": 401, "message": "Authentication failed"}})
    data = request.get_json()
    target_temperature = data['target_temperature']
    api.device_repository.set_target_temperature(ObjectId(device_id), target_temperature)
    device = api.device_repository.get_device_by_id(ObjectId(device_id))
    return jsonify({
        "device": device.get_device_attributes(),
        "error": None
    })


@api.route('/device/<string:device_id>/switch/configure', methods=['POST'])
def configure_switch(device_id, token):
    access = api.device_repository.validate_token(ObjectId(device_id), token)
    if access is False:
        return jsonify({"device": None, "error": {"code": 401, "message": "Authentication failed"}})
    data = request.get_json()
    power_state = data['power_state']
    api.device_repository.set_power_state(ObjectId(device_id), power_state)
    device = api.device_repository.get_device_by_id(ObjectId(device_id))
    return jsonify({
        "device": device.get_device_attributes(),
        "error": None
    })


@api.route('/devices/faulty')
def faulty_devices():
    faulty_devices = api.device_repository.get_faulty_devices()
    return jsonify({
        "devices": [x.get_device_attributes() for x in faulty_devices],
        "error": None
    })


from admin import *


def main():
    setup_cron()
    api.run(debug=True, host=api.config['HOSTNAME'], port=int(api.config['PORT']))


if __name__ == "__main__":
    main()

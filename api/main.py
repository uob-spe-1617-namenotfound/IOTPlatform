import json
import logging

from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
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
api.trigger_repository = api.repository_collection.trigger_repository
api.token_repository = api.repository_collection.token_repository


def get_request_token():
    return request.get_json()['token']


@api.route('/user/<string:user_id>')
def get_user_info(user_id):
    access = api.token_repository.authenticate_user(ObjectId(user_id), get_request_token())
    if access is False:
        return jsonify({"user": None, "error": {"code": 401, "message": "Authentication failed"}})
    user = api.user_repository.get_user_by_id(ObjectId(user_id))
    if user is None:
        return jsonify({"user": None, "error": {"code": 404, "message": "No such user found"}})
    return jsonify({"user": user.get_user_attributes(), "error": None})


@api.route('/users')
def get_all_users():
    access = api.token_repository.authenticate_admin(get_request_token())
    if access is False:
        return jsonify({"users": None, "error": {"code": 401, "message": "Authentication failed"}})
    users = api.user_repository.get_all_users()
    return jsonify({"users": [user.get_user_attributes() for user in users], "error": None})


@api.route('/user/<string:user_id>/house', methods=['POST'])
def get_house_for_user(user_id):
    access = api.token_repository.authenticate_user(ObjectId(user_id), get_request_token())
    if access is False:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    logging.debug("Getting house for user {}".format(user_id))
    house = api.house_repository.get_houses_for_user(ObjectId(user_id))[0]
    if house is None:
        return jsonify({"house": None, "error": {"code": 404, "message": "No such House found"}})
    return jsonify({"house": house.get_house_attributes(), "error": None})


@api.route('/room/<string:room_id>')
def get_room_info(room_id):
    access = api.room_repository.validate_token(ObjectId(room_id), get_request_token())
    if access is False:
        return jsonify({"room": None, "error": {"code": 401, "message": "Authentication failed"}})
    room = api.room_repository.get_room_by_id(ObjectId(room_id))
    if room is None:
        return jsonify({"room": None, "error": {"code": 404, "message": "No such room found"}})
    return jsonify({"room": room.get_room_attributes(), "error": None})


@api.route('/house/<string:house_id>/rooms', methods=['POST'])
def get_rooms_for_house(house_id):
    access = api.house_repository.validate_token(ObjectId(house_id), get_request_token())
    if access is False:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    rooms = api.room_repository.get_rooms_for_house(ObjectId(house_id))
    if rooms is None:
        return jsonify({"rooms": None, "error": {"code": 404, "message": "No such house found"}})
    return jsonify({"rooms": [room.get_room_attributes() for room in rooms], "error": None})


@api.route('/room/<string:room_id>/devices')
def get_devices_for_room(room_id):
    access = api.room_repository.validate_token(ObjectId(room_id), get_request_token())
    if access is False:
        return jsonify({"room": None, "error": {"code": 401, "message": "Authentication failed"}})
    devices = api.device_repository.get_devices_for_room(ObjectId(room_id))
    if devices is None:
        return jsonify({"devices": None, "error": {"code": 404, "message": "No such room found"}})
    return jsonify({"devices": [device.get_device_attributes() for device in devices], "error": None})


@api.route('/house/<string:house_id>/devices')
def get_devices_for_house(house_id):
    access = api.house_repository.validate_token(ObjectId(house_id), get_request_token())
    if access is False:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    devices = api.device_repository.get_devices_for_house(ObjectId(house_id))
    if devices is None:
        return jsonify({"devices": None, "error": {"code": 404, "message": "No such house found"}})
    return jsonify({"devices": [device.get_device_attributes() for device in devices], "error": None})


@api.route('/device/<string:device_id>')
def get_device_info(device_id):
    access = api.device_repository.validate_token(ObjectId(device_id), get_request_token())
    if access is False:
        return jsonify({"device": None, "error": {"code": 401, "message": "Authentication failed"}})
    device = api.device_repository.get_device_by_id(ObjectId(device_id))
    if device is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such device found"}})
    return jsonify({"device": device.get_device_attributes(), "error": None})


@api.route('/house/<string:house_id>/devices/add', methods=['POST'])
def add_device(house_id):
    access = api.house_repository.validate_token(ObjectId(house_id), get_request_token())
    if access is False:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    house = api.house_repository.get_house_by_id(ObjectId(house_id))
    if house is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such house found"}})
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
def remove_device(device_id):
    access = api.device_repository.validate_token(ObjectId(device_id), get_request_token())
    if access is False:
        return jsonify({"device_id": None, "error": {"code": 401, "message": "Authentication failed"}})
    result = api.device_repository.remove_device(ObjectId(device_id))
    if result is None:
        return jsonify({"device_id": None, "error": {"code": 404, "message": "No such device found"}})
    return jsonify({"device_id": result.device_id, "error": None})


@api.route('/house/<string:house_id>/rooms/add', methods=['POST'])
def add_room(house_id):
    access = api.house_repository.validate_token(ObjectId(house_id), get_request_token())
    if access is False:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    logging.debug("Authentication success")
    data = request.get_json()
    room_id = api.room_repository.add_room(ObjectId(house_id), data['name'])
    room = api.room_repository.get_room_by_id(room_id)
    return jsonify({"room": room.get_room_attributes(), "error": None})


@api.route('/room/<string:room_id>/device/<string:device_id>/link')
def link_device_to_room(room_id, device_id):
    access1 = api.room_repository.validate_token(ObjectId(room_id), get_request_token())
    access2 = api.device_repository.validate_token(ObjectId(device_id), get_request_token())
    if access1 is False or access2 is False:
        return jsonify({"device": None, "error": {"code": 401, "message": "Authentication failed"}})
    room = api.room_repository.get_room_by_id(ObjectId(room_id))
    if room is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such room found"}})
    result = api.device_repository.link_device_to_room(ObjectId(room_id), ObjectId(device_id))
    if result is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such device found."}})
    return jsonify({"device": result.get_device_attributes(), "error": None})


@api.route('/device/<string:device_id>/triggers/add', methods=['POST'])
def add_trigger(device_id):
    access = api.device_repository.validate_token(ObjectId(device_id), get_request_token())
    if access is False:
        return jsonify({"trigger": None, "error": {"code": 401, "message": "Authentication failed"}})
    device = api.device_repository.get_device_by_id(ObjectId(device_id))
    if device is None:
        return jsonify({"trigger": None, "error": {"code": 404, "message": "No such device found"}})
    data = request.get_json()
    trigger = data['trigger']
    actor_id = data['actor_id']
    action = data['action']
    result = api.trigger_repository.add_trigger(ObjectId(device_id), trigger, ObjectId(actor_id), action)
    if result is None:
        return jsonify({"trigger": None, "error": {"code": 404, "message": "Trigger couldn't be created."}})
    return jsonify({"trigger": result.get_trigger_attributes(), "error": None})


@api.route('/device/<string:device_id>/thermostat/configure', methods=['POST'])
def configure_thermostat(device_id):
    access = api.device_repository.validate_token(ObjectId(device_id), get_request_token())
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
def configure_switch(device_id):
    access = api.device_repository.validate_token(ObjectId(device_id), get_request_token())
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


@api.route('/house/<string:house_id>')
def location_attr(house_id):
    access = api.house_repository.validate_token(ObjectId(house_id), get_request_token())
    if access is False:
        return jsonify({"devices": None, "error": {"code": 401, "message": "Authentication failed"}})
    attributes = api.house_repository.get_house_attributes(house_id)
    attributes['location'] = {'lat': 51.529249, 'lng': -0.117973, 'description': 'University of Bristol'}
    return attributes


@api.route('/user/<string:user_id>/faults')
def faulty_user_devices(user_id):
    access = api.token_repository.authenticate_admin(get_request_token())
    if access is False:
        return jsonify({"devices": None, "error": {"code": 401, "message": "Authentication failed"}})
    faulty_devices = api.user_repository.get_faulty_devices_for_user(user_id)
    devices = []
    if faulty_devices is None:
        return jsonify({"devices": None, "error": None})
    else:
        for device in faulty_devices:
            attributes = device.get_device_attributes()
            faulty_device = dict()
            faulty_device['user_id'] = attributes['user_id']
            faulty_device['device_id'] = attributes['device_id']
            faulty_device['device_type'] = attributes['device_type']
            faulty_device['vendor'] = attributes['vendor']
            faulty_device['fault'] = attributes['fault']
            devices.append(faulty_device)
        return jsonify({"devices": devices, "error": None})


@api.route('/admin/faults')
def all_faulty_devices():
    access = api.token_repository.authenticate_admin(get_request_token())
    if access is False:
        return jsonify({"devices": None, "error": {"code": 401, "message": "Authentication failed"}})
    devices = []
    faulty_devices = api.device_repository.get_faulty_devices()
    if faulty_devices is None:
        return jsonify({"devices": None, "error": None})
    else:
        for device in faulty_devices:
            attributes = device.get_device_attributes()
            faulty_device = dict()
            faulty_device['user_id'] = attributes['user_id']
            faulty_device['device_id'] = attributes['device_id']
            faulty_device['device_type'] = attributes['device_type']
            faulty_device['vendor'] = attributes['vendor']
            faulty_device['fault'] = attributes['fault']
            devices.append(faulty_device)
        return jsonify({"devices": devices, "error": None})


@api.route('/admin/graph')
def get_weekly_consumption():
    access = api.token_repository.authenticate_admin(get_request_token())
    if access is False:
        return jsonify({"consumption": None, "error": {"code": 401, "message": "Authentication failed"}})
    devices = api.user_repository.get_all_devices()
    for device in devices:
        dev = api.device_repository.get_device_by_id(device['_id'])
        device_consumption = dev.get_energy_readings()
    pass


bcrypt = Bcrypt(api)


@api.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    email_address, password = login_data['email_address'], login_data['password']
    data = dict()
    logging.debug("API login, received data: {} {}".format(email_address, password))
    login_user = api.user_repository.get_user_by_email(email_address)
    if login_user is not None:
        logging.debug("Checking password hash")
        if bcrypt.check_password_hash(login_user.password_hash, password):
            logging.debug("Password hash matched")
            token = api.token_repository.generate_token(login_user.user_id)
            logging.debug("Token generated: {}".format(token))
            data['result'] = {'success': True, 'admin': login_user.is_admin, 'user_id': login_user.user_id,
                              'token': token}
            data['error'] = None
        else:
            data['success'] = False
            data['error'] = {'code': 406, 'message': 'Password is incorrect'}
    else:
        data['success'] = False
        data['error'] = {'code': 404, 'message': 'Username not found'}
    return jsonify(data)


@api.route('/register', methods=['POST'])
def register():
    registration = request.get_json()
    data = dict()
    logging.debug("Data: {}".format(registration))
    user = api.user_repository.get_user_by_email(registration['email_address'])
    logging.debug("Found user: {}".format(user))
    if user is not None:
        data['success'] = False
        data['error'] = {'code': 409, 'message': 'Email address is already registered'}
    else:
        if registration['password'] is not None:
            logging.debug("Password!")
            hashed_password = bcrypt.generate_password_hash(registration['password']).decode('utf-8')
            logging.debug("Hashed: {}".format(hashed_password))
            new_user = api.user_repository.add_user(registration['name'], hashed_password,
                                                    registration['email_address'], False)
            logging.debug("New user: {}".format(new_user))
            house_id = api.house_repository.add_house(new_user, "{}'s house".format(registration['name']), None)
            logging.debug("Add house: {}".format(house_id))
            data['result'] = {'success': True, 'user_id': str(new_user), 'house_id': str(house_id)}
            data['error'] = None
    return jsonify(data)


@api.route('/logout', methods=['POST'])
def logout():
    access = api.token_repository.check_token_validity(get_request_token())
    if access is False:
        return jsonify({"devices": None, "error": {"code": 401, "message": "Authentication failed"}})
    api.token_repository.invalidate_token(get_request_token())
    valid = api.token_repository.check_token_validity(get_request_token())
    if valid is False:
        return jsonify({"success": True, "error": None})
    else:
        return jsonify({"success": False, "error": {"code": 401, "message": "Logout failed"}})


from admin import *


def main():
    setup_cron()
    api.run(debug=True, host=api.config['HOSTNAME'], port=int(api.config['PORT']))


if __name__ == "__main__":
    main()

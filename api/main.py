import datetime
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
api.trigger_repository = api.repository_collection.trigger_repository
api.theme_repository = api.repository_collection.theme_repository
api.token_repository = api.repository_collection.token_repository


def get_request_token():
    return request.get_json()['token']


@api.route('/user/<string:user_id>', methods=['POST'])
def get_user_info(user_id):
    access = api.token_repository.authenticate_user(ObjectId(user_id), get_request_token())
    if not access:
        return jsonify({"user": None, "error": {"code": 401, "message": "Authentication failed"}})
    user = api.user_repository.get_user_by_id(ObjectId(user_id))
    if user is None:
        return jsonify({"user": None, "error": {"code": 404, "message": "No such user found"}})
    return jsonify({"user": user.get_user_attributes(), "error": None})


@api.route('/graph/<user_id>', methods=['POST'])
def get_user_graph_data(user_id):
    access = api.token_repository.authenticate_user(ObjectId(user_id), get_request_token())
    if not access:
        return jsonify({"data": None, "error": {"code": 401, "message": "Authentication failed"}})
    user = api.user_repository.get_user_by_id(ObjectId(user_id))
    if user is None:
        return jsonify({"data": None, "error": {"code": 404, "message": "No such user found"}})

    base = datetime.datetime.today()
    numdays = 30

    dateList = []
    for x in range(0, numdays):
        dateList.append(base - datetime.timedelta(days=x))

    readingList = []
    for y in range(0, numdays):
        readingList.append(round(7.845, 2))  # remain constant for now, 7.845 is a random value.

    data = {date.strftime("%d-%B-%Y"): data for date, data in zip(dateList, readingList)}

    return jsonify({"data": data, "error": None})


@api.route('/users', methods=['POST'])
def get_all_users():
    access = api.token_repository.authenticate_admin(get_request_token())
    if not access:
        return jsonify({"users": None, "error": {"code": 401, "message": "Authentication failed"}})
    users = api.user_repository.get_all_users()
    return jsonify({"users": [user.get_user_attributes() for user in users], "error": None})


@api.route('/user/<string:user_id>/house', methods=['POST'])
def get_house_for_user(user_id):
    access = api.token_repository.authenticate_user(ObjectId(user_id), get_request_token())
    if not access:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    logging.debug("Getting house for user {}".format(user_id))
    house = api.house_repository.get_houses_for_user(ObjectId(user_id))[0]
    if house is None:
        return jsonify({"house": None, "error": {"code": 404, "message": "No such House found"}})
    return jsonify({"house": house.get_house_attributes(), "error": None})


@api.route('/room/<string:room_id>', methods=['POST'])
def get_room_info(room_id):
    access = api.room_repository.validate_token(ObjectId(room_id), get_request_token())
    if not access:
        return jsonify({"room": None, "error": {"code": 401, "message": "Authentication failed"}})
    room = api.room_repository.get_room_by_id(ObjectId(room_id))
    if room is None:
        return jsonify({"room": None, "error": {"code": 404, "message": "No such room found"}})
    return jsonify({"room": room.get_room_attributes(), "error": None})


@api.route('/house/<string:house_id>/rooms', methods=['POST'])
def get_rooms_for_house(house_id):
    access = api.house_repository.validate_token(ObjectId(house_id), get_request_token())
    if not access:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    rooms = api.room_repository.get_rooms_for_house(ObjectId(house_id))
    if rooms is None:
        return jsonify({"rooms": None, "error": {"code": 404, "message": "No such house found"}})
    return jsonify({"rooms": [room.get_room_attributes() for room in rooms], "error": None})


@api.route('/room/<string:room_id>/devices', methods=['POST'])
def get_devices_for_room(room_id):
    access = api.room_repository.validate_token(ObjectId(room_id), get_request_token())
    if not access:
        return jsonify({"room": None, "error": {"code": 401, "message": "Authentication failed"}})
    devices = api.device_repository.get_devices_for_room(ObjectId(room_id))
    if devices is None:
        return jsonify({"devices": None, "error": {"code": 404, "message": "No such room found"}})
    return jsonify({"devices": [device.get_device_attributes() for device in devices], "error": None})


@api.route('/house/<string:house_id>/devices', methods=['POST'])
def get_devices_for_house(house_id):
    access = api.house_repository.validate_token(ObjectId(house_id), get_request_token())
    if not access:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    devices = api.device_repository.get_devices_for_house(ObjectId(house_id))
    if devices is None:
        return jsonify({"devices": None, "error": {"code": 404, "message": "No such house found"}})
    return jsonify({"devices": [device.get_device_attributes() for device in devices], "error": None})


@api.route('/device/<string:device_id>', methods=['POST'])
def get_device_info(device_id):
    access = api.device_repository.validate_token(ObjectId(device_id), get_request_token())
    if not access:
        return jsonify({"device": None, "error": {"code": 401, "message": "Authentication failed"}})
    device = api.device_repository.get_device_by_id(ObjectId(device_id))
    if device is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such device found"}})
    return jsonify({"device": device.get_device_attributes(), "error": None})


@api.route('/house/<string:house_id>/devices/add', methods=['POST'])
def add_device(house_id):
    access = api.house_repository.validate_token(ObjectId(house_id), get_request_token())
    if not access:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    house = api.house_repository.get_house_by_id(ObjectId(house_id))
    if house is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such house found"}})
    data = request.get_json()
    logging.debug("Adding device: {}".format(data))
    device_id = api.device_repository.add_device(house_id=ObjectId(house_id),
                                                 room_id=None,
                                                 name=data['name'],
                                                 device_type=data['device_type'],
                                                 target=data['target'],
                                                 configuration=data['configuration'],
                                                 vendor=data['vendor'])
    device = api.device_repository.get_device_by_id(device_id)
    logging.debug("Device added: {}".format(device))
    if device is None:
        return jsonify({"device": None, "error": {"code": 400, "message": "Device could not be added"}})
    return jsonify({"device": device.get_device_attributes(), "error": None})


@api.route('/device/<string:device_id>/remove', methods=['POST'])
def remove_device(device_id):
    access = api.device_repository.validate_token(ObjectId(device_id), get_request_token())
    if not access:
        return jsonify({"device_id": None, "error": {"code": 401, "message": "Authentication failed"}})
    result = api.device_repository.remove_device(ObjectId(device_id))
    if result is None:
        return jsonify({"device_id": None, "error": {"code": 404, "message": "No such device found"}})
    return jsonify({"device_id": result.device_id, "error": None})


@api.route('/house/<string:house_id>/rooms/add', methods=['POST'])
def add_room(house_id):
    logging.debug("Add new room to house: {}".format(house_id))
    logging.debug("JSON: {}".format(request.get_json()))
    access = api.house_repository.validate_token(ObjectId(house_id), get_request_token())
    if not access:
        return jsonify({"house": None, "error": {"code": 401, "message": "Authentication failed"}})
    data = request.get_json()
    room_id = api.room_repository.add_room(ObjectId(house_id), data['name'])
    room = api.room_repository.get_room_by_id(room_id)
    return jsonify({"room": room.get_room_attributes(), "error": None})


@api.route('/room/<string:room_id>/remove', methods=['POST'])
def remove_room(room_id):
    access = api.room_repository.validate_token(ObjectId(room_id), get_request_token())
    if not access:
        return jsonify({"room_id": None, "error": {"code": 401, "message": "Authentication failed"}})
    result = api.room_repository.remove_room(ObjectId(room_id))
    if result is None:
        return jsonify({"room_id": None, "error": {"code": 404, "message": "No such room found"}})
    return jsonify({"room_id": result.room_id, "error": None})


@api.route('/room/<string:room_id>/device/<string:device_id>/link', methods=['POST'])
def link_device_to_room(room_id, device_id):
    access1 = api.room_repository.validate_token(ObjectId(room_id), get_request_token())
    access2 = api.device_repository.validate_token(ObjectId(device_id), get_request_token())
    if not access1 or not access2:
        return jsonify({"device": None, "error": {"code": 401, "message": "Authentication failed"}})
    room = api.room_repository.get_room_by_id(ObjectId(room_id))
    if room is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such room found"}})
    result = api.device_repository.link_device_to_room(ObjectId(room_id), ObjectId(device_id))
    if result is None:
        return jsonify({"device": None, "error": {"code": 404, "message": "No such device found."}})
    return jsonify({"device": result.get_device_attributes(), "error": None})


@api.route('/device/<string:device_id>/thermostat/configure', methods=['POST'])
def configure_thermostat(device_id):
    access = api.device_repository.validate_token(ObjectId(device_id), get_request_token())
    if not access:
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
    if not access:
        return jsonify({"device": None, "error": {"code": 401, "message": "Authentication failed"}})
    data = request.get_json()
    power_state = data['power_state']
    api.device_repository.set_power_state(ObjectId(device_id), power_state)
    device = api.device_repository.get_device_by_id(ObjectId(device_id))
    return jsonify({
        "device": device.get_device_attributes(),
        "error": None
    })


@api.route('/house/<string:house_id>', methods=['POST'])
def get_house_info(house_id):
    access = api.house_repository.validate_token(ObjectId(house_id), get_request_token())
    if not access:
        return jsonify({"devices": None, "error": {"code": 401, "message": "Authentication failed"}})
    house = api.house_repository.get_house_by_id(house_id)
    return jsonify({
        "house": house,
        "error": None
    })


@api.route('/trigger/<string:trigger_id>', methods=['POST'])
def get_trigger_info(trigger_id):
    access = api.trigger_repository.validate_token(ObjectId(trigger_id), get_request_token())
    if not access:
        return jsonify({"trigger": None, "error": {"code": 401, "message": "Authentication failed"}})
    trigger = api.trigger_repository.get_trigger_by_id(ObjectId(trigger_id))
    if trigger is None:
        return jsonify({"trigger": None, "error": {"code": 404, "message": "No such trigger found"}})
    return jsonify({"trigger": trigger.get_trigger_attributes(), "error": None})


@api.route('/device/<string:device_id>/triggers', methods=['POST'])
def get_triggers_for_device(device_id):
    access = api.device_repository.validate_token(ObjectId(device_id))
    if not access:
        return jsonify({"triggers": None, "error": {"code": 401, "message": "Authentication failed"}})
    triggers = api.trigger_repository.get_triggers_for_device(ObjectId(device_id))
    if triggers is None:
        return jsonify({"triggers": None, "error": {"code": 404, "message": "No triggers found"}})
    return jsonify({"triggers": [trigger.get_trigger_attributes() for trigger in triggers], "error": None})


@api.route('/device/<string:device_id>/actions', methods=['POST'])
def get_actions_for_device(device_id):
    access = api.device_repository.validate_token(ObjectId(device_id))
    if not access:
        return jsonify({"triggers": None, "error": {"code": 401, "message": "Authentication failed"}})
    triggers = api.trigger_repository.get_actions_for_device(ObjectId(device_id))
    if triggers is None:
        return jsonify({"triggers": None, "error": {"code": 404, "message": "No triggers found"}})
    return jsonify({"triggers": [trigger.get_trigger_attributes() for trigger in triggers], "error": None})


@api.route('/trigger/create', methods=['POST'])
def add_new_trigger():
    data = request.get_json()
    access1 = api.device_repository.validate_token(ObjectId(data['sensor_id']), get_request_token())
    access2 = api.device_repository.validate_token(ObjectId(data['actor_id']), get_request_token())
    if not access1 or not access2:
        return jsonify({"trigger": None, "error": {"code": 401, "message": "Authentication failed"}})
    sensor = api.device_repository.get_device_by_id(ObjectId(data['sensor_id']))
    actor = api.device_repository.get_device_by_id(ObjectId(data['actor_id']))
    if sensor is None:
        return jsonify({"trigger": None, "error": {"code": 404, "message": "No such sensor found"}})
    if actor is None:
        return jsonify({"trigger": None, "error": {"code": 404, "message": "No such actor found"}})
    trigger_id = api.trigger_repository.add_trigger(ObjectId(data['sensor_id']), data['event'], data['event_params'],
                                                    ObjectId(data['actor_id']), data['action'], data['action_params'],
                                                    ObjectId(data['user_id']))
    trigger = api.trigger_repository.get_trigger_by_id(trigger_id)
    if trigger is None:
        return jsonify({"trigger": None, "error": {"code": 400, "message": "Trigger could not be added"}})
    return jsonify({"trigger": trigger.get_trigger_attributes(), "error": None})


@api.route('/trigger/<string:trigger_id>/edit', methods=['POST'])
def edit_trigger(trigger_id):
    data = request.get_json()
    access1 = api.trigger_repository.validate_token(ObjectId(trigger_id), get_request_token())
    access2 = api.device_repository.validate_token(ObjectId(data['sensor_id']), get_request_token())
    access3 = api.device_repository.validate_token(ObjectId(data['actor_id']), get_request_token())
    if not access1 or not access2 or not access3:
        return jsonify({"trigger": None, "error": {"code": 401, "message": "Authentication failed"}})
    trigger = api.trigger_repository.get_trigger_by_id(ObjectId(trigger_id))
    if trigger is None:
        return jsonify({"trigger": None, "error": {"code": 404, "message": "No such trigger found"}})
    trigger = api.trigger_repository.edit_trigger(ObjectId(trigger_id), data['event'], data['event_params'],
                                                  data['action'], data['action_params'])
    return jsonify({"trigger": trigger.get_trigger_attributes(), "error": None})


@api.route('/trigger/<string:trigger_id>/delete', methods=['POST'])
def remove_trigger(trigger_id):
    access = api.trigger_repository.validate_token(ObjectId(trigger_id), get_request_token())
    if not access:
        return jsonify({"trigger": None, "error": {"code": 401, "message": "Authentication failed"}})
    result = api.trigger_repository.remove_trigger(ObjectId(trigger_id))
    if result is None:
        return jsonify({"trigger": None, "error": {"code": 404, "message": "No such trigger found"}})
    return jsonify({"trigger": trigger.trigger_id, "error": None})


@api.route('/user/<string:user_id>/triggers', methods=['POST'])
def get_triggers_for_user(user_id):
    access = api.token_repository.validate_token(ObjectId(user_id), get_request_token())
    if not access:
        return jsonify({"triggers": None, "error": {"code": 401, "message": "Authentication failed"}})
    triggers = api.trigger_repository.get_triggers_for_user(ObjectId(user_id))
    if triggers is None:
        return jsonify({"triggers": None, "error": {"code": 404, "message": "No triggers found for this user"}})
    return jsonify({"triggers": triggers, "error": None})


@api.route('/user/<string:user_id>/themes', methods=['POST'])
def get_themes_for_user(user_id):
    access = api.token_repository.validate_token(ObjectId(user_id), get_request_token())
    if not access:
        return jsonify({"themes": None, "error": {"code": 401, "message": "Authentication failed"}})
    themes = api.theme_repository.get_themes_for_user(ObjectId(user_id))
    if themes is None:
        return jsonify({"themes": None, "error": {"code": 404, "message": "No themes found for this user"}})
    return jsonify({"themes": themes, "error": None})


@api.route('/theme/<string:theme_id>', methods=['POST'])
def get_theme_info(theme_id):
    access = api.theme_repository.validate_token(ObjectId(theme_id), get_request_token())
    if not access:
        return jsonify({"theme": None, "error": {"code": 401, "message": "Authentication failed"}})
    theme = api.theme_repository.get_theme_by_id(ObjectId(theme_id))
    if theme is None:
        return jsonify({"theme": None, "error": {"code": 404, "message": "No such theme found"}})
    return jsonify({"theme": theme.get_theme_attributes(), "error": None})


@api.route('/theme/create', methods=['POST'])
def add_new_theme():
    data = request.get_json()
    for dev_id in data['settings']:
        access = api.device_repository.validate_token(ObjectId(dev_id), get_request_token())
        if not access:
            return jsonify({"theme": None, "error": {"code": 401, "message": "Authentication failed"}})
    theme_id = api.theme_repository.add_theme(ObjectId(data['user_id']), data['name'], data['settings'],
                                              ObjectId(data['active']))
    theme = api.theme_repository.get_theme_by_id(theme_id)
    if theme is None:
        return jsonify({"theme": None, "error": {"code": 400, "message": "Theme could not be added"}})
    return jsonify({"theme": theme.get_theme_attributes(), "error": None})


@api.route('/theme/<string:theme_id>/edit', methods=['POST'])
def edit_theme(theme_id):
    data = request.get_json()
    for dev_id in data['settings']:
        access = api.device_repository.validate_token(ObjectId(dev_id), get_request_token())
        if not access:
            return jsonify({"theme": None, "error": {"code": 401, "message": "Authentication failed"}})
    theme = api.theme_repository.get_theme_by_id(theme_id)
    if theme is None:
        return jsonify({"theme": None, "error": {"code": 404, "message": "No such theme found"}})
    theme = api.theme_repository.edit_theme(theme_id, data['settings'], data['active'])
    return jsonify({"theme": theme.get_theme_attributes(), "error": None})


@api.route('/theme/<string:theme_id>/device/<string:device_id>/update')
def update_theme(theme_id, device_id, setting):
    access = api.theme_repository.validate_token(ObjectId(theme_id), get_request_token())
    if not access:
        return jsonify({"theme": None, "error": {"code": 401, "message": "Authentication failed"}})
    theme = api.theme_repository.get_theme_by_id(theme_id)
    if device_id not in theme.settings:
        updated_theme = theme.add_device_to_theme(theme_id, device_id, setting)
    else:
        updated_theme = theme.edit_device_settings(theme_id, device_id, setting)
    return jsonify({"theme": updated_theme.get_theme_attributes(), "error": None})


@api.route('/theme/<string:theme_id>/device/<string:device_id>/remove', methods=['POST'])
def remove_device_from_theme(theme_id, device_id):
    access = api.theme_repository.validate_token(ObjectId(theme_id), get_request_token())
    if not access:
        return jsonify({"theme": None, "error": {"code": 401, "message": "Authentication failed"}})
    theme = api.theme_repository.remove_device_from_theme(theme_id, device_id)
    return jsonify({"theme": theme, "error": None})


@api.route('/theme/<string:theme_id>/delete', methods=['POST'])
def remove_theme(theme_id):
    access = api.theme_repository.validate_token(ObjectId(theme_id), get_request_token())
    if not access:
        return jsonify({"theme": None, "error": {"code": 401, "message": "Authentication failed"}})
    result = api.theme_repository.remove_theme(ObjectId(theme_id))
    if result is None:
        return jsonify({"theme": None, "error": {"code": 404, "message": "No such theme found"}})
    return jsonify({"theme": result.theme_id, "error": None})


@api.route('/theme/<string:theme_id>/activate', methods=['POST'])
def activate_theme(theme_id):
    access = api.theme_repository.validate_token(ObjectId(theme_id), get_request_token())
    if not access:
        return jsonify({"theme": None, "error": {"code": 401, "message": "Authentication failed"}})
    theme = api.theme_repository.get_theme_by_id(theme_id)
    for dev_id in theme.settings:
        access = api.device_repository.validate_token(ObjectId(dev_id), get_request_token())
        if not access:
            return jsonify({"theme": None, "error": {"code": 401, "message": "Authentication failed"}})
    result = api.theme_repository.change_theme_state(theme_id, True)
    return jsonify({"theme": result, "error": None})


@api.route('/theme/<string:theme_id>/deactivate', methods=['POST'])
def deactivate_theme(theme_id):
    access = api.theme_repository.validate_token(ObjectId(theme_id), get_request_token())
    if not access:
        return jsonify({"theme": None, "error": {"code": 401, "message": "Authentication failed"}})
    theme = api.theme_repository.get_theme_by_id(theme_id)
    for dev_id in theme.settings:
        access = api.device_repository.validate_token(ObjectId(dev_id), get_request_token())
        if not access:
            return jsonify({"theme": None, "error": {"code": 401, "message": "Authentication failed"}})
    result = api.theme_repository.change_theme_state(theme_id, False)
    return jsonify({"theme": result, "error": None})


@api.route('/user/<string:user_id>/faults', methods=['POST'])
def faulty_user_devices(user_id):
    access = api.token_repository.authenticate_admin(get_request_token())
    if not access:
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


@api.route('/admin/faults', methods=['POST'])
def all_faulty_devices():
    access = api.token_repository.authenticate_admin(get_request_token())
    if not access:
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
def get_overall_consumption():
    access = api.token_repository.authenticate_admin(get_request_token())
    if not access:
        return jsonify({"consumption": None, "error": {"code": 401, "message": "Authentication failed"}})
    overall_consumption = api.device_repository.get_overall_consumption()
    if overall_consumption is None:
        return jsonify(
            {"consumption": None, "error": {"code": 404, "message": "Overall consumption could not be obtained"}})
    return jsonify({"consumption": overall_consumption, "error": None})


@api.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    email_address, password = login_data['email_address'], login_data['password']
    data = dict()
    logging.debug("API login, received data: {} {}".format(email_address, password))
    try:
        login_user = api.user_repository.check_password(email_address=email_address, password=password)
        token = api.token_repository.generate_token(login_user.user_id)
        logging.debug("Token generated: {}".format(token))
        data['result'] = {'success': True, 'admin': login_user.is_admin, 'user_id': login_user.user_id,
                          'token': token}
        data['error'] = None
    except repositories.RepositoryException as ex:
        data['success'] = False
        data['error'] = ex.error_data
    return jsonify(data)


@api.route('/register', methods=['POST'])
def register():
    registration = request.get_json()
    data = dict()
    logging.debug("Data: {}".format(registration))
    try:
        new_user = api.user_repository.register_new_user(registration['email_address'], registration['password'],
                                                         registration['name'], False)
        logging.debug("New user: {}".format(new_user))
        house_id = api.house_repository.add_house(new_user, "{}'s house".format(registration['name']), None)
        logging.debug("Add house: {}".format(house_id))
        data['result'] = {'success': True, 'user_id': str(new_user), 'house_id': str(house_id)}
        data['error'] = None
    except repositories.RepositoryException as ex:
        data['result'] = {'success': False}
        data['error'] = ex.error_data
    return jsonify(data)


@api.route('/logout', methods=['POST'])
def logout():
    access = api.token_repository.check_token_validity(get_request_token())
    if not access:
        return jsonify({"devices": None, "error": {"code": 401, "message": "Authentication failed"}})
    api.token_repository.invalidate_token(get_request_token())
    valid = api.token_repository.check_token_validity(get_request_token())
    if not valid:
        return jsonify({"success": True, "error": None})
    else:
        return jsonify({"success": False, "error": {"code": 401, "message": "Logout failed"}})


from admin import *


def main():
    setup_cron()
    api.run(debug=True, host=api.config['HOSTNAME'], port=int(api.config['PORT']))


if __name__ == "__main__":
    main()

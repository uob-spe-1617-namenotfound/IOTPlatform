import logging

import requests

import utilities.session
from main import app


def get_api_url(endpoint):
    return "http://{}:{}{}".format(app.config['API_HOSTNAME'], app.config['API_PORT'], endpoint)


def get_user_id():
    user = utilities.session.get_active_user()
    logging.debug("Current user: {}".format(user))
    if user is None or 'user_id' not in user:
        return None
    return user['user_id']


def get_default_house_id():
    return get_current_user_house()['house_id']


def get_current_user_house():
    return get_house_for_user(get_user_id())


def get_authentication_token():
    return {"token": utilities.session.get_active_user_token()}


def get_house_for_user(user_id):
    r = requests.post(get_api_url('/user/{}/house'.format(user_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['house']


def get_user_default_rooms():
    r = requests.post(get_api_url('/house/{}/rooms'.format(get_default_house_id())),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['rooms']


def get_house_id_for_user(user_id):
    return get_house_for_user(user_id)["house_id"]


def get_rooms_for_user(user_id):
    r = requests.post(get_api_url('/house/{}/rooms'.format(get_house_id_for_user(user_id))),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['rooms']


def add_new_device(user_id, name, device_type, vendor, configuration):
    sending_data = {"name": name,
                    "configuration": configuration,
                    "device_type": device_type,
                    "vendor": vendor,
                    "token": utilities.session.get_active_user_token()}
    r = requests.post(get_api_url('/house/{}/devices/add'.format(get_house_id_for_user(user_id))),
                      json=sending_data)
    logging.debug("Received from add new device: {}".format(r.content))
    try:
        data = r.json()
    except:
        logging.debug("Parsing response to JSON failed!")
        raise Exception("JSON parse error")
    if data['error'] is not None:
        raise Exception("Error!")
    return data['device']['device_id']


def add_new_room(user_id, name):
    r = requests.post(get_api_url('/house/{}/rooms/add'.format(get_house_id_for_user(user_id))),
                      json={"name": name,
                            "token": utilities.session.get_active_user_token()})
    logging.debug(r.content)
    try:
        data = r.json()
    except:
        logging.debug("Parsing response to JSON failed!")
        raise Exception("JSON parse error")
    logging.debug("Name of room: {}".format(data['room']['name']))
    if data['error'] is not None:
        raise Exception("Error!")
    return data['room']['room_id']


def get_user_devices(user_id):
    return get_house_devices(get_house_id_for_user(user_id))


def get_house_devices(house_id):
    r = requests.post(get_api_url('/house/{}/devices'.format(house_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data["devices"]


def get_room_devices(room_id):
    r = requests.post(get_api_url('/room/{}/devices'.format(room_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['devices']


def link_device_to_room(room_id, device_id):
    r = requests.post(get_api_url('/room/{}/device/{}/link'.format(room_id, device_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['device']['device_id']


def move_device2room(device2room):
    return None


def get_house_info(house_id):
    r = requests.post(get_api_url('/house/{}'.format(house_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['house']


def get_room_info(room_id):
    r = requests.post(get_api_url('/room/{}'.format(room_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['room']


def remove_room(room_id):
    r = requests.post(get_api_url('/room/{}/remove'.format(room_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['trigger']


def get_device_info(device_id):
    r = requests.post(get_api_url('/device/{}'.format(device_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['device']


def set_thermostat_target(device_id, target_temperature):
    r = requests.post(get_api_url('/device/{}/thermostat/configure'.format(device_id)),
                      json={"target_temperature": target_temperature,
                            "token": utilities.session.get_active_user_token()})
    print(r.content)
    data = r.json()
    if data['error'] is not None:
        raise Exception('Error!')
    return data['device']


def set_switch_state(device_id, state):
    r = requests.post(get_api_url('/device/{}/switch/configure'.format(device_id)),
                      json={"power_state": state,
                            "token": utilities.session.get_active_user_token()})
    print(r.content)
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['device']


def add_new_trigger(sensor_id, event, event_params, actor_id, action, action_params, user_id):
    r = requests.post(get_api_url('/trigger/create'),
                      json={"sensor_id": sensor_id,
                            "event": event,
                            "event_params": event_params,
                            "actor_id": actor_id,
                            "action": action,
                            "action_params": action_params,
                            "user_id": user_id,
                            "token": utilities.session.get_active_user_token()})
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['trigger']


def get_trigger_info(trigger_id):
    r = requests.post(get_api_url('/trigger/{}'.format(trigger_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['trigger']


def get_possible_affected_devices(device_id):
    device_info = get_device_info(device_id)
    all_devices = get_house_devices(device_info["house_id"])
    all_affected_devices = get_affected_triggers(device_id)
    logging.info("All affected devices: {}".format(all_affected_devices))
    invalid_devices = {device["actor_id"] for device in all_affected_devices} | {device_id} | {
        device["device_id"] for device in all_devices if device["device_type"] in ["motion_sensor"]
    }
    return [device for device in all_devices if (device["device_id"] not in invalid_devices)]


def load_trigger_devices_data(triggers):
    for t in triggers:
        t["sensor_info"] = get_device_info(t["sensor_id"])
        t["actor_info"] = get_device_info(t["actor_id"])


def get_affecting_triggers(device_id):
    r = requests.post(get_api_url('/device/{}/triggers'.format(device_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    triggers = data['triggers']
    load_trigger_devices_data(triggers)
    return triggers


def get_affected_triggers(device_id):
    r = requests.post(get_api_url('/device/{}/actions'.format(device_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    triggers = data['triggers']
    load_trigger_devices_data(triggers)
    return triggers


def edit_trigger(trigger_id, event, event_params, action, action_params):
    r = requests.post(get_api_url('/trigger/{}/edit').format(trigger_id),
                      json={"event": event,
                            "event_params": event_params,
                            "action": action,
                            "action_params": action_params,
                            "token": utilities.session.get_active_user_token()})
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['trigger']


def remove_trigger(trigger_id):
    r = requests.post(get_api_url('/trigger/{}/delete').format(trigger_id),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['trigger']


def get_triggers_for_user(user_id):
    r = requests.post(get_api_url('/user/{}/triggers').format(user_id),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    triggers = data['triggers']
    load_trigger_devices_data(triggers)
    return triggers


def get_admin_fault_status():
    r = requests.post(get_api_url('/admin/faults'),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception('Error!')
    return data['devices']


def get_user_faulty_devices(user_id):
    r = requests.get(get_api_url('user/{}/faulty').format(user_id),
                     json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception('Error!')
    return data['devices']


def get_user_info(user_id):
    r = requests.post(get_api_url("/user/{}".format(user_id)),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data["user"]


def get_all_users():
    r = requests.post(get_api_url("/users"),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['users']


def get_overall_power_consumption():
    r = requests.get(get_api_url('/admin/graph'),
                     json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception('Error!')
    return data['devices']


def logout():
    r = requests.post(get_api_url("/logout"),
                      json=get_authentication_token())
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['success']

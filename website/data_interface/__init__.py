import logging

import requests

from main import app


def get_api_url(endpoint):
    return "http://{}:{}{}".format(app.config['API_HOSTNAME'], app.config['API_PORT'], endpoint)


def get_user_id():
    # TODO: remove once login functionality has been made
    r = requests.get(get_api_url('/user/default_user'))
    data = r.json()
    return data['user_id']


def get_default_house_id():
    return get_current_user_houses()[0]["house_id"]


def get_current_user_houses():
    return get_houses_for_user(get_user_id())


def get_houses_for_user(user_id):
    r = requests.get(get_api_url('/user/{}/houses'.format(user_id)))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['houses']


def get_user_default_rooms():
    r = requests.get(get_api_url('/house/{}/rooms'.format(get_default_house_id())))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['rooms']


def get_default_house_id_for_user(user_id):
    return get_houses_for_user(user_id)[0]["house_id"]


def get_default_rooms_for_user(user_id):
    r = requests.get(get_api_url('/house/{}/rooms'.format(get_default_house_id_for_user(user_id))))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['rooms']


def add_new_device(name, device_type, vendor, configuration):
    r = requests.post(get_api_url('/house/{}/devices/add'.format(get_default_house_id())),
                      json={"name": name,
                            "configuration": configuration,
                            "device_type": device_type,
                            "vendor": vendor})
    logging.debug("Received from add new device: {}".format(r.content))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['device']['_id']


def add_new_room(name):
    r = requests.post(get_api_url('/house/{}/rooms/add'.format(get_default_house_id())),
                      json={"name": name})
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['room']['room_id']


def get_user_default_devices():
    r = requests.get(get_api_url('/house/{}/devices'.format(get_default_house_id())))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data["devices"]


def get_room_devices(room_id):
    r = requests.get(get_api_url('/room/{}/devices'.format(room_id)))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['devices']


def link_device_to_room(room_id, device_id):
    r = requests.get(get_api_url('/room/{}/device/{}/link'.format(room_id, device_id)))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['device']['device_id']


def get_house_info(house_id):
    r = requests.get(get_api_url('/house/{}'.format(house_id)))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['house']


def get_room_info(room_id):
    r = requests.get(get_api_url('/room/{}'.format(room_id)))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['room']


def get_device_info(device_id):
    r = requests.get(get_api_url('/device/{}'.format(device_id)))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['device']


def set_thermostat_target(device_id, target_temperature):
    r = requests.post(get_api_url('/device/{}/thermostat/configure'.format(device_id)),
                      json={"target_temperature": target_temperature})
    print(r.content)
    data = r.json()
    if data['error'] is not None:
        raise Exception('Error!')
    return data['device']


def set_switch_state(device_id, state):
    r = requests.post(get_api_url('/device/{}/switch/configure'.format(device_id)),
                      json={"power_state": state})
    print(r.content)
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['device']


def get_faulty_devices():
    r = requests.get(get_api_url('/devices/faulty'))
    data = r.json()
    if data['error'] is not None:
        raise Exception('Error!')
    return data['devices']


def get_user_info(user_id):
    r = requests.get(get_api_url("/user/{}".format(user_id)))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data["user"]


def get_all_users():
    r = requests.get(get_api_url("/users"))
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['users']

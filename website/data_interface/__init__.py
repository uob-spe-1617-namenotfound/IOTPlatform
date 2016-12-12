import requests
from flask import session

from website import app


def get_api_url(endpoint):
    return "http://{}:{}{}".format(app.config['API_HOSTNAME'], app.config['API_PORT'], endpoint)


def get_user_id():
    # TODO: remove once login functionality has been made
    session['user_id'] = 'user_id_1'
    if "user_id" in session:
        return session['user_id']
    return None


def get_default_house_id():
    return get_user_houses()[0]["house_id"]


def get_user_houses():
    r = requests.get(get_api_url('/user/{}/houses'.format(get_user_id())))
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


def add_new_device(name, device_type, vendor, configuration):
    r = requests.post(get_api_url('/house/{}/devices/add'.format(get_default_house_id())),
                      json={"name": name, "configuration": configuration, "device_type": device_type, "vendor": vendor})
    data = r.json()
    if data['error'] is not None:
        raise Exception("Error!")
    return data['device']['device_id']


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

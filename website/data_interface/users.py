import requests

import data_interface


def register_user(email_address, password, name):
    r = requests.post(data_interface.get_api_url('/register'),
                      json={"email_address": email_address,
                            "password": password,
                            "name": name})
    data = r.json()
    return data['result'], data['error']


def login(email_address, password):
    r = requests.post(data_interface.get_api_url('/login'),
                      json={"email_address": email_address, "password": password})
    data = r.json()
    if data['error'] is not None:
        return None, data['error']
    error = None
    user_id = data['result']['user_id']
    admin = data['result']['admin']
    token = data['result']['token']
    result = {
        "user_id": user_id,
        "admin": admin,
        "token": token
    }
    return result, error

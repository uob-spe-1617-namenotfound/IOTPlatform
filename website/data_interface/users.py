import requests

from data_interface import get_api_url, get_default_user_id


def register_user(email_address, password, name):
    r = requests.post(get_api_url('/register'),
                      json={"email_address": email_address,
                            "password": password,
                            "name": name})
    data = r.json()
    if data['error'] is not None:
        raise Exception('Error!')
    return data['result'], data['error']


def login(email_address, password):
    error = None
    # TODO: don't login default user (blocked by API: feature request #2)

    user_id = get_default_user_id()
    admin = False

    result = {
        "user_id": user_id,
        "admin": admin
    }
    return result, error

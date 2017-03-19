import data_interface


def register_user(email_address, password, name):
    result = None
    error = "Registration is not implemented in the API yet"
    return result, error


def login(email_address, password):
    error = None
    # TODO: don't login default user (blocked by API: feature request #2)

    user_id = data_interface.get_default_user_id()
    admin = False

    result = {
        "user_id": user_id,
        "admin": admin
    }
    return result, error

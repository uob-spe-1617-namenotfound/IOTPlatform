from flask import session


def login(user_id, token, is_admin=False):
    session['active_user'] = {
        "user_id": user_id,
        "admin": is_admin,
        "token": token
    }
    return None


def logout():
    session['active_user'] = None


def get_active_user():
    if 'active_user' not in session:
        return None
    return session['active_user']


def get_active_user_token():
    user = get_active_user()
    if user is None:
        return None
    return user['token']


def is_user_logged_in():
    user = get_active_user()
    if user is None:
        return False
    if 'admin' not in user:
        return True
    if user['admin']:
        return False
    return True


def is_admin_logged_in():
    user = get_active_user()
    if user is None:
        return False
    if 'admin' not in user:
        return False
    if user['admin']:
        return True
    return False

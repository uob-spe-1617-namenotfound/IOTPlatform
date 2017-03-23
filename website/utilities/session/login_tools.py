from functools import wraps

from flask import redirect, flash, url_for

import utilities.session


def user_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if utilities.session.is_user_logged_in():
            return f(*args, **kwargs)
        else:
            flash('You need to be logged in as a user.', 'danger')
            if utilities.session.is_admin_logged_in():
                return redirect(url_for('admin.index'))
            return redirect(url_for('public.login'))

    return wrap

def admin_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if utilities.session.is_admin_logged_in():
            return f(*args, **kwargs)
        else:
            flash('You need to be logged in as an admin.', 'danger')
            if utilities.session.is_user_logged_in():
                return redirect(url_for('internal.index'))
            return redirect(url_for('public.login'))
    return wrap
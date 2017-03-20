from flask import Blueprint

from internal.navbar import internal_navbar as navbar
from utilities.session.login_tools import user_login_required

internal_site = Blueprint('internal', __name__, template_folder='../templates/internal')


@internal_site.before_request
@user_login_required
def before_request():
    pass


import internal.views

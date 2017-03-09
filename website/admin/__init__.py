from flask import Blueprint

from admin.navbar import admin_navbar as navbar
from utilities.session.login_tools import admin_login_required

admin_site = Blueprint('admin', __name__, template_folder='../templates/admin')


@admin_site.before_request
@admin_login_required
def before_request():
    pass


import admin.views

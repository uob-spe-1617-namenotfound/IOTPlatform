from flask import Blueprint

from admin.navbar import admin_navbar as navbar

admin_site = Blueprint('admin', __name__, template_folder='../templates/admin')

import admin.views

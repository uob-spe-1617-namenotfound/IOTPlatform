from flask import Blueprint
from internal.navbar import internal_navbar as navbar

internal_site = Blueprint('internal', __name__, template_folder='../templates/internal')

import internal.views

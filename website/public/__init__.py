from flask import Blueprint

from public.navbar import public_navbar as navbar

public_site = Blueprint('public', __name__)

import public.views
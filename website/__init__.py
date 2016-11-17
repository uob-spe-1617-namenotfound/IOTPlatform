from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav

from website.navbar import navbar

app = Flask("SPE-IoT-Energy", template_folder="website/templates")
app.config.from_pyfile('config.cfg')
Bootstrap(app)

nav = Nav(app)

nav.register_element('navbar', navbar)

import website.views

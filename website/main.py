import logging

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav, register_renderer

app = Flask("SPE-IoT-Energy", template_folder="templates")
app.config.from_pyfile('config.cfg')
logging.basicConfig(level=logging.DEBUG)
Bootstrap(app)

nav = Nav()

# Import blueprints
import admin, internal, public

# Register blueprints
app.register_blueprint(admin.admin_site, url_prefix='/admin')
app.register_blueprint(internal.internal_site, url_prefix='/internal')
app.register_blueprint(public.public_site)

from utilities.ui.bootstrap import CustomBootstrapRenderer
from utilities.ui import timestamp_to_date_time
app.add_template_filter(timestamp_to_date_time, "timestamp_to_str")

register_renderer(app, 'custom_bootstrap_nav', CustomBootstrapRenderer)
nav.register_element('public_navbar', public.navbar)
nav.register_element('admin_navbar', admin.navbar)
nav.register_element('internal_navbar', internal.navbar)
nav.init_app(app)


def main():
    app.run(host=app.config['HOSTNAME'], port=int(app.config['PORT']))


if __name__ == "__main__":
    main()

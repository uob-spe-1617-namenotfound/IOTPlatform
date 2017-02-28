from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
import logging

from navbar import navbar

app = Flask("SPE-IoT-Energy", template_folder="templates")
app.config.from_pyfile('config.cfg')
logging.basicConfig(level=logging.DEBUG)
Bootstrap(app)

nav = Nav(app)

nav.register_element('navbar', navbar)

from views import *

def main():
    app.run(host=app.config['HOSTNAME'], port=int(app.config['PORT']))
        
if __name__ == "__main__":
    main()

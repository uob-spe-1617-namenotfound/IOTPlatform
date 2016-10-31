from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

Bootstrap(app)

app.config.update(
    DEBUG=True,
    HOSTNAME="0.0.0.0"
)


@app.route('/')
def index():
    return "Hello, world!"


app.run(host=app.config['HOSTNAME'])

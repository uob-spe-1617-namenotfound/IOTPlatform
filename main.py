from flask import Flask

app = Flask(__name__)

app.config.update(
    DEBUG=True
)


@app.route('/')
def index():
    return "Hello, world!"


app.run()

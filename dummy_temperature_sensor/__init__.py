from datetime import datetime

from flask import Flask, jsonify

app = Flask("SPE-IoT-Dummy-Temperature-Sensor")
app.config.from_pyfile('config.cfg')


@app.route('/read')
@app.route('/<int:device_id>/read')
def read(device_id=None):
    temperature = 21.6
    if device_id is not None:
        temperature += device_id
    return jsonify({
        "data": {
            "temperature": temperature,
            "timestamp": datetime.now()
        },
        "error": None
    })


def main():
    app.run(host=app.config['HOSTNAME'], port=int(app.config['PORT']))


if __name__ == "__main__":
    main()
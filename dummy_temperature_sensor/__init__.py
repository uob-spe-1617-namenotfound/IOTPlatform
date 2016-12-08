from datetime import datetime

from flask import Flask, jsonify

app = Flask("SPE-IoT-Dummy-Temperature-Sensor")
app.config.from_pyfile('config.cfg')


@app.route('/read')
def read():
    return jsonify({
        "data": {
            "temperature": 21.6,
            "timestamp": datetime.now()
        },
        "error": None
    })


def main():
    app.run(host=app.config['HOSTNAME'], port=int(app.config['PORT']))


if __name__ == "__main__":
    main()
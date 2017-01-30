from datetime import datetime

from flask import Flask, jsonify, request

app = Flask("SPE-IoT-Dummy-Temperature-Sensor")
app.config.from_pyfile('config.cfg')

targets = dict()
motion_data = dict()


@app.route('/thermostat')
@app.route('/thermostat/<int:device_id>')
def read_thermostat(device_id=None):
    temperature = 21.6
    if device_id is not None:
        temperature += device_id
    target = 24
    if device_id in targets:
        target = targets[device_id]
    return jsonify({
        "data": {
            "temperature": temperature,
            "target": target,
            "timestamp": datetime.now()
        },
        "error": None
    })


@app.route('/faulty_thermostat/read')
def faulty_thermostat():
    return jsonify({
        "data": None,
        "error": "No data available"
    })


@app.route('/thermostat/<int:device_id>/write', methods=['POST'])
def write_thermostat_target(device_id):
    data = request.get_json()
    targets[device_id] = data['target_temperature']
    return jsonify({"error": None})


@app.route('/motion_sensor')
@app.route('/motion_sensor/<int:device_id>')
def read_motion_sensor(device_id=None):
    motion = False
    if device_id is not None and device_id in motion_data:
        motion = motion_data[device_id]
    return jsonify({
        "data": {
            "motion": motion,
            "timestamp": datetime.now()
        },
        "error": None
    })


def main():
    app.run(host=app.config['HOSTNAME'], port=int(app.config['PORT']))


if __name__ == "__main__":
    main()

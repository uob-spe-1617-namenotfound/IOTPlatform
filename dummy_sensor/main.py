import logging
import random
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask("SPE-IoT-Dummy-Temperature-Sensor")
app.config.from_pyfile('config.cfg')
logging.basicConfig(level=logging.DEBUG)


@app.route('/thermostat')
@app.route('/thermostat/<int:device_id>')
def read_thermostat(device_id=None):
    temperature = random.randint(0, 100) + random.randint(0, 100) * .01
    if device_id in app.thermostat_temperatures:
        temperature = app.thermostat_temperatures[device_id]
    target = 24
    if device_id in app.thermostat_target_temperatures:
        target = app.thermostat_target_temperatures[device_id]
    logging.debug("Retrieving target temperature for device {}: {}".format(device_id, target))
    return jsonify({
        "data": {
            "temperature": temperature,
            "target": target,
            "timestamp": datetime.now()
        },
        "error": None
    })


@app.route('/faulty_thermostat')
def faulty_thermostat():
    return jsonify({
        "data": None,
        "error": "No data available"
    })


@app.route('/faulty_thermostat/write', methods=['POST'])
def write_faulty_thermostat():
    return jsonify({
        "error": "Can't write to thermostat"
    })


@app.route('/thermostat/<int:device_id>/write', methods=['POST'])
def write_thermostat_target(device_id):
    data = request.get_json()
    app.thermostat_target_temperatures[device_id] = data['target_temperature']
    logging.debug(
        "Set target temperature for device {} to {}".format(device_id, app.thermostat_target_temperatures[device_id]))
    return jsonify({"error": None})


@app.route('/thermostat/<int:device_id>/write/<string:value>')
def write_thermostat_target_value(device_id, value):
    app.thermostat_target_temperatures[device_id] = float(value)
    return jsonify({
        "error": None
    })


@app.route('/thermostat/<int:device_id>/temperature/write/<string:value>')
def write_thermostat_temperature(device_id, value):
    app.thermostat_temperatures[device_id] = float(value)
    return jsonify({
        "error": None
    })


@app.route('/motion_sensor')
@app.route('/motion_sensor/<int:device_id>')
def read_motion_sensor(device_id=None):
    motion = False
    if device_id is not None and device_id in app.motion_sensor_data:
        motion = app.motion_sensor_data[device_id]
    return jsonify({
        "data": {
            "motion": motion,
            "timestamp": datetime.now()
        },
        "error": None
    })


@app.route('/motion_sensor/<int:device_id>/write/<string:value>')
def write_motion_sensor_value(device_id, value):
    app.motion_sensor_data[device_id] = (value == "1")
    return jsonify({
        "error": None
    })


@app.route('/open_sensor')
@app.route('/open_sensor/<int:device_id>')
def read_open_sensor(device_id=None):
    open_state = False
    if device_id is not None and device_id in app.open_sensor_data:
        open_state = app.open_sensor_data[device_id]
    return jsonify({
        "data": {
            "state": open_state,
            "timestamp": datetime.now()
        },
        "error": None
    })


@app.route('/open_sensor/<int:device_id>/write/<string:value>')
def write_open_sensor_value(device_id, value):
    app.open_sensor_data[device_id] = (value == "1")
    return jsonify({
        "error": None
    })


@app.route('/light_switch')
@app.route('/light_switch/<int:device_id>')
def read_light_switch(device_id=None):
    power_state = False
    if device_id is not None and device_id in app.light_switch_data:
        power_state = app.light_switch_data[device_id]
    return jsonify({
        "data": {
            "state": power_state,
            "timestamp": datetime.now()
        },
        "error": None
    })


@app.route('/light_switch/<int:device_id>/write', methods=['POST'])
def write_light_switch(device_id):
    app.light_switch_data[device_id] = bool(request.get_json()['power_state'])
    return jsonify({
        "error": None
    })


@app.route('/light_switch/<int:device_id>/write/<string:value>')
def write_light_switch_value(device_id, value):
    app.light_switch_data[device_id] = (value == "1")
    return jsonify({
        "error": None
    })


def main():
    app.light_switch_data = dict()
    app.open_sensor_data = dict()
    app.thermostat_target_temperatures = dict()
    app.thermostat_temperatures = dict()
    app.motion_sensor_data = dict()
    app.run(host=app.config['HOSTNAME'], port=int(app.config['PORT']))


if __name__ == "__main__":
    main()

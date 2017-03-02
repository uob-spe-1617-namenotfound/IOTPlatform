from flask import render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, DecimalField
from wtforms.validators import URL

import data_interface
from main import app


class PairNewDeviceForm(FlaskForm):
    name = StringField("Device name")
    device_type = SelectField("Device type", choices=[('motion_sensor', "Motion sensor"), ('thermostat', "Thermostat"),
                                                      ('light_switch', "Light switch"),
                                                      ('door_sensor', "Door/Window Sensor")])
    url = StringField("API URL", validators=[URL(require_tld=False)])
    submit = SubmitField()


motion_triggers = [{'id': '00', 'name': 'When Motion is Detected'},
                   {'id': '01', 'name': 'When No Motion is Detected'}]
thermostat_triggers = [{'id': '000', 'name': 'When the temperature is above 22'},
                       {'id': '1111', 'name': 'When temperature is below 15'}]
light_triggers = [{'id': '0000', 'name': 'Lights are on for 4 hours'}]
door_triggers = [{'id': 'opens', 'name': "Opens"}, {'id': 'closes', 'name': "Closes"}]

paireddevices = [
    {'text': 'Bathroom Thermostat', 'device_id': '10', 'type': 'thermostat', 'trigger': thermostat_triggers},
    {'text': 'Kitchen Thermostat', 'device_id': '20', 'type': 'thermostat', 'trigger': thermostat_triggers},
    {'text': 'Dining Room Thermostat', 'device_id': '30', 'type': 'thermostat', 'trigger': thermostat_triggers},
    {'text': 'Dining Room Motion Sensor', 'id': '40', 'type': 'motion_sensor', 'trigger': motion_triggers},
    {'text': 'Bedroom Motion Sensor', 'id': '50', 'type': 'motion_sensor', 'trigger': motion_triggers},
    {'text': 'Bathroom Light Switch', 'id': '60', 'type': 'light_switch', 'trigger': light_triggers}]

groupactions = ['Turn On', 'Turn Off', 'Set Temperature']
groups = [{'id': '11', 'name': 'Ground Floor Thermostats', 'device_ids': [paireddevices[1], paireddevices[2]],
           'group_actions': [groupactions[0], groupactions[1], groupactions[2]]},
          {'id': '21', 'name': 'Motion In Bedrooms', 'device_ids': [paireddevices[3]],
           'group_actions': [groupactions[0], groupactions[1]]},
          {'id': '31', 'name': 'Lighting in First Floor', 'device_ids': [paireddevices[4]],
           'group_actions': [groupactions[0], groupactions[1]]}]

actions = {"door_sensor": ['Turn on', 'Turn Off', 'No Action'],
           "light_switch": ['Turn Switch on', 'Turn Switch Off', 'No Action'],
           "thermostat": ['Turn on', 'Turn Off', 'No Action', 'Modify Temperature'],
           "motion_sensor": ['Turn on', 'Turn Off', 'No Action']}


@app.route('/devices')
def show_devices():
    devices = data_interface.get_user_default_devices()
    return render_template("devices.html", paireddevices=devices, groups=groups, groupactions=groupactions)


@app.route('/devices/new', methods=['POST', 'GET'])
def add_new_device():
    form = PairNewDeviceForm()
    if form.validate_on_submit():
        data_interface.add_new_device(device_type=form.device_type.data, vendor="OWN",
                                      configuration={"url": form.url.data},
                                      name=form.name.data)
        flash("New device successfully added!", 'success')
        return redirect(url_for('.show_devices'))
    return render_template("new_device.html", new_device_form=form)


class SetThermostatTargetForm(FlaskForm):
    target_temperature = DecimalField("Target temperature ℃")
    submit = SubmitField()


@app.route('/device/<string:device_id>')
def show_device(device_id, form=None):
    triggers = None
    device = data_interface.get_device_info(device_id)
    if device['device_type'] == "thermostat":
        triggers = thermostat_triggers
        if form is None:
            form = SetThermostatTargetForm()
    elif device['device_type'] == "motion_sensor":
        triggers = motion_triggers
    elif device['device_type'] == "light_switch":
        triggers = light_triggers
    elif device['device_type'] == "door_sensor":
        triggers = door_triggers
    all_user_devices = data_interface.get_user_default_devices()
    actors = [{"id": device['device_id'], "name": device['name'], "type": "device", "device": device,
               "action": actions[device['device_type']]} for device in
              all_user_devices] + [{"id": "webhook_url", "type": "webhook", "url": "#", "name": "Send email"}]
    thermostats = filter(lambda x: x['device_id'] == "thermostat", all_user_devices)
    door_sensors = filter(lambda x: x['device_id'] == "door_sensor", all_user_devices)
    motion_sensors = filter(lambda x: x['device_id'] == "motion_sensor", all_user_devices)
    light_switches = filter(lambda x: x['device_id'] == "light_switch", all_user_devices)
    return render_template("deviceactions.html", device=device, triggers=triggers, actors=actors,
                           thermostats=thermostats, light_switches=light_switches, door_sensors=door_sensors,
                           motion_sensors=motion_sensors, change_settings_form=form)


@app.route('/device/<string:device_id>/configure', methods=['POST'])
def set_device_settings(device_id):
    form = SetThermostatTargetForm()
    if form.validate_on_submit():
        data_interface.set_thermostat_target(device_id, float(form.target_temperature.data))
        flash('Target temperature successfully set!', 'success')
        return redirect(url_for('.show_device', device_id=device_id))
    return show_device(device_id, form)


@app.route('/device/<string:device_id>/switch/configure/<int:state>')
def set_switch_settings(device_id, state):
    error = data_interface.set_switch_state(device_id, state)
    if error is not None:
        flash("State successfully set", "success")
    return redirect(url_for('.show_device', device_id=device_id))

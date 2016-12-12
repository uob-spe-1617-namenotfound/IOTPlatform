from flask import render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import URL
from website import data_interface
from website.views import thermostattriggers, motiontriggers, lighttriggers
from website import app


class PairNewDeviceForm(FlaskForm):
    name = StringField("Device name")
    device_type = SelectField("Device type", choices=[('motion_sensor', "Motion sensor"), ('thermostat', "Thermostat"),
                                                      ('light_switch', "Light switch"),
                                                      ('door_sensor', "Door/Window Sensor")])
    url = StringField("API URL", validators=[URL(require_tld=False)])
    submit = SubmitField()


paireddevices = [
    {'text': 'Bathroom Thermostat', 'device_id': '10', 'type': 'thermostat', 'trigger': thermostattriggers},
    {'text': 'Kitchen Thermostat', 'device_id': '20', 'type': 'thermostat', 'trigger': thermostattriggers},
    {'text': 'Dining Room Thermostat', 'device_id': '30', 'type': 'thermostat', 'trigger': thermostattriggers},
    {'text': 'Dining Room Motion Sensor', 'id': '40', 'type': 'motion_sensor', 'trigger': motiontriggers},
    {'text': 'Bedroom Motion Sensor', 'id': '50', 'type': 'motion_sensor', 'trigger': motiontriggers},
    {'text': 'Bathroom Light Switch', 'id': '60', 'type': 'light_switch', 'trigger': lighttriggers}]

groupactions = ['Turn On', 'Turn Off', 'Set Temperature']
groups = [{'id': '11', 'name': 'Ground Floor Thermostats', 'device_ids': [paireddevices[1], paireddevices[2]],
           'group_actions': [groupactions[0], groupactions[1], groupactions[2]]},
          {'id': '21', 'name': 'Motion In Bedrooms', 'device_ids': [paireddevices[3]],
           'group_actions': [groupactions[0], groupactions[1]]},
          {'id': '31', 'name': 'Lighting in First Floor', 'device_ids': [paireddevices[4]],
           'group_actions': [groupactions[0], groupactions[1]]}]


@app.route('/devices')
def devices():
    devices = data_interface.get_user_default_devices()
    return render_template("devices.html", paireddevices=devices, groups=groups, groupactions=groupactions)


@app.route('/devices/new', methods=['POST', 'GET'])
def add_new_device():
    form = PairNewDeviceForm()
    if form.validate_on_submit():
        data_interface.add_new_device(device_type=form.device_type.data, vendor="OWN", configuration={"url": form.url.data},
                                      name=form.name.data)
        flash("New device successfully added!", 'success')
        return redirect(url_for('.devices'))
    return render_template("new_device.html", new_device_form=form)

from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, SelectField, StringField, DecimalField
from wtforms.validators import URL


class AddNewRoomForm(FlaskForm):
    name = StringField("Room name", [validators.Length(min=1)])
    submit = SubmitField()


class AddNewDeviceForm(FlaskForm):
    name = StringField("Device name", [validators.Length(min=1)])
    device_type = SelectField("Device type", choices=[('motion_sensor', "Motion sensor"), ('thermostat', "Thermostat"),
                                                      ('light_switch', "Light switch"),
                                                      ('door_sensor', "Door/Window Sensor")])
    url = StringField("API URL", validators=[URL(require_tld=False)])
    submit = SubmitField()


class SetThermostatTargetForm(FlaskForm):
    target_temperature = DecimalField("Target temperature ℃")
    submit = SubmitField()

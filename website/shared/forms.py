from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, SelectField, StringField, DecimalField, HiddenField
from wtforms.validators import URL, InputRequired


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


class CreateTriggerForm(FlaskForm):
    affected_device = SelectField("Affected device")

    def __init__(self, possible_affected_devices):
        FlaskForm.__init__(self)
        self.affected_device.choices = [(device["device_id"], device["name"]) for device in possible_affected_devices]


class CreateTriggerFormThermostat(CreateTriggerForm):
    event = SelectField("Event",
                        choices=[("temperature_gets_higher_than", "Temperature gets higher than"),
                                 ("temperature_gets_lower_than", "Temperature gets lower than")],
                        validators=[InputRequired()])
    event_parameters = DecimalField("Temperature", validators=[InputRequired()])
    submit = SubmitField()


class CreateTriggerFormMotionSensor(CreateTriggerForm):
    event = SelectField("Event",
                        choices=[("motion_detected_start", "Start motion"),
                                 ("motion_detected_stop", "End of motion")],
                        validators=[InputRequired()])
    event_parameters = HiddenField()
    submit = SubmitField()


class CreateTriggerFormDoorSensor(CreateTriggerForm):
    pass


class CreateTriggerActionFormThermostat(FlaskForm):
    action = SelectField("Action", choices=[("set_target_temperature", "Set target temperature")],
                         validators=[InputRequired()])
    action_parameters = DecimalField("Temperature", validators=[InputRequired()])
    event = HiddenField()
    event_parameters = HiddenField()
    submit = SubmitField()

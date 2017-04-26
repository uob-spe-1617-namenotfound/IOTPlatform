from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, SelectField, StringField, PasswordField
from wtforms.validators import InputRequired


def get_device_types(light_switch=True, motion_sensor=True, door_sensor=True, thermostat=True):
    result = []
    if light_switch:
        result.append(("light_switch", "Light switch"))
    if motion_sensor:
        result.append(("motion_sensor", "Motion sensor"))
    if door_sensor:
        result.append(("door_sensor", "Door sensor"))
    if thermostat:
        result.append(("thermostat", "Thermostat"))
    return result


class NewDeviceVendorOwnForm(FlaskForm):
    name = StringField("Device name", [validators.Length(min=1)])
    device_type = SelectField("Device type", choices=get_device_types(), validators=[InputRequired()])
    configuration_url = StringField("API URL", [validators.URL(require_tld=False)])
    submit = SubmitField()


class NewDeviceVendorEnergenieForm(FlaskForm):
    name = StringField("Device name", [validators.InputRequired()])
    device_type = SelectField("Device type",
                              choices=get_device_types(door_sensor=False,
                                                       motion_sensor=False,
                                                       light_switch=True,
                                                       thermostat=True))
    configuration_username = StringField("Energenie username", [validators.InputRequired()])
    configuration_password = PasswordField("Energenie password", [validators.InputRequired()])
    configuration_device_id = StringField("Energenie device id", [validators.InputRequired()])
    submit = SubmitField()


all_vendors = {
    "1": {
        "name": "OWN",
        "form": NewDeviceVendorOwnForm,
        "backend_id": "OWN",
        "get_configuration_data_function": (lambda f: {"url": f.configuration_url.data})
    },
    "2": {
        "name": "Energenie",
        "form": NewDeviceVendorEnergenieForm,
        "backend_id": "energenie",
        "get_configuration_data_function": (lambda f: {"password": f.configuration_password.data,
                                                       "username": f.configuration_username.data,
                                                       "device_id": f.configuration_device_id.data})
    }
}


def get_vendor_backend_id(vendor_id):
    return all_vendors[vendor_id]["backend_id"]


def get_vendor_form(vendor_id):
    t = all_vendors[vendor_id]["form"]
    return t()


def get_all_vendors_list():
    return [{
        "name": all_vendors[k]["name"],
        "id": k,
        "form": get_vendor_form(k)
    } for k in sorted(all_vendors.keys())]


def get_vendor_configuration_data(vendor_id, form):
    return all_vendors[vendor_id]["get_configuration_data_function"](form)

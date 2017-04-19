from flask import render_template, flash, redirect, url_for

import data_interface
from internal import internal_site
from internal.views.forms import AddNewDeviceForm, SetThermostatTargetForm



motion_triggers = [{'id': '00', 'name': 'When Motion is Detected'},
                   {'id': '01', 'name': 'When No Motion is Detected'}]
thermostat_triggers = [{'id': '000', 'name': 'When the temperature is above 22'},
                       {'id': '1111', 'name': 'When temperature is below 15'}]
light_triggers = [{'id': '0000', 'name': 'Lights are on for 4 hours'}]
door_triggers = [{'id': 'opens', 'name': "Opens"}, {'id': 'closes', 'name': "Closes"}]


groupactions = ['Turn On', 'Turn Off', 'Set Temperature']

actions = {"door_sensor": ['Turn on', 'Turn Off', 'No Action'],
           "light_switch": ['Turn Switch on', 'Turn Switch Off', 'No Action'],
           "thermostat": ['Turn on', 'Turn Off', 'No Action', 'Modify Temperature'],
           "motion_sensor": ['Turn on', 'Turn Off', 'No Action']}


@internal_site.route('/devices')
def show_devices():
    form = AddNewDeviceForm()
    devices = data_interface.get_user_default_devices()
    rooms = data_interface.get_user_default_rooms()
    rooms = sorted(rooms, key=lambda k: k['name'])
    any_linked = False
    any_unlinked = False
    moveinfo = []
    if devices:
        for device in devices:
            if device['room_id'] != None:
                any_linked = True
            elif device['room_id'] == None:
                any_unlinked = True
    #change from default to focal user
    #test requires here to check if devices returns devices correctly
    return render_template("internal/devices.html", moveinfo=moveinfo, devices=devices, groupactions=groupactions, rooms=rooms, new_device_form=form, table1=any_unlinked, table2=any_linked)


@internal_site.route('/devices/new', methods=['POST', 'GET'])
def add_new_device():
    form = AddNewDeviceForm()
    if form.validate_on_submit():
        data_interface.add_new_device(device_type=form.device_type.data, vendor="OWN",
                                      configuration={"url": form.url.data},
                                      name=form.name.data)
        flash("New device successfully added!", 'success')
        return redirect(url_for('.show_devices'))
    return render_template("internal/new_device.html", new_device_form=form)





@internal_site.route('/device/<string:device_id>')
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
    return render_template("internal/deviceactions.html", device=device, triggers=triggers, actors=actors,
                           thermostats=thermostats, light_switches=light_switches, door_sensors=door_sensors,
                           motion_sensors=motion_sensors, change_settings_form=form)


@internal_site.route('/device/<string:device_id>/configure', methods=['POST'])
def set_device_settings(device_id):
    form = SetThermostatTargetForm()
    if form.validate_on_submit():
        data_interface.set_thermostat_target(device_id, float(form.target_temperature.data))
        flash('Target temperature successfully set!', 'success')
        return redirect(url_for('.show_device', device_id=device_id))
    return show_device(device_id, form)


@internal_site.route('/device/<string:device_id>/switch/configure/<int:state>')
def set_switch_settings(device_id, state):
    error = data_interface.set_switch_state(device_id, state)
    if error is not None:
        flash("State successfully set", "success")
    return redirect(url_for('.show_device', device_id=device_id))

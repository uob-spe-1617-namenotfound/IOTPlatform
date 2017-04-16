from flask import render_template, flash, redirect, url_for

import data_interface
import shared.actions
import shared.triggers
from admin import admin_site
from shared.forms import AddNewDeviceForm, SetThermostatTargetForm


@admin_site.route('/user/<string:user_id>/devices')
def show_devices(user_id):
    form = AddNewDeviceForm()
    devices = data_interface.get_user_devices(user_id)
    rooms = data_interface.get_rooms_for_user(user_id)
    rooms = sorted(rooms, key=lambda k: k['name'])
    any_linked = False
    any_unlinked = False
    if devices:
        for device in devices:
            if device['room_id'] != None:
                any_linked = True
            elif device['room_id'] == None:
                any_unlinked = True
    # TODO: change from default to focal user
    # TODO: test requires here to check if devices returns devices correctly
    return render_template("admin/admin_devices.html", devices=devices, groupactions=groupactions, rooms=rooms,
                           new_device_form=form, table1=any_unlinked, table2=any_linked)


@admin_site.route('/user/<string:user_id>/devices/new', methods=['POST', 'GET'])
def add_new_device(user_id):
    form = AddNewDeviceForm()
    if form.validate_on_submit():
        data_interface.add_new_device(user_id=user_id, device_type=form.device_type.data, vendor="OWN",
                                      configuration={"url": form.url.data},
                                      name=form.name.data)
        flash("New device successfully added by Admin!", 'success')
        return redirect(url_for('.show_devices', user_id=user_id))
    return render_template("admin/admin_new_device.html", new_device_form=form)


@admin_site.route('/user/<string:user_id>/device/<string:device_id>')
def show_device(user_id, device_id, form=None):
    user = data_interface.get_user_info(user_id)
    triggers = None
    device = data_interface.get_device_info(device_id)
    if device['device_type'] == "thermostat":
        triggers = shared.triggers.thermostat_triggers
        if form is None:
            form = SetThermostatTargetForm()
    elif device['device_type'] == "motion_sensor":
        triggers = shared.triggers.motion_triggers
    elif device['device_type'] == "light_switch":
        triggers = shared.triggers.light_triggers
    elif device['device_type'] == "door_sensor":
        triggers = shared.triggers.door_triggers
    all_user_devices = data_interface.get_user_devices(user_id)
    actors = [{"id": device['device_id'], "name": device['name'], "type": "device", "device": device,
               "action": shared.actions.actions[device['device_type']]} for device in
              all_user_devices] + [{"id": "webhook_url", "type": "webhook", "url": "#", "name": "Send email"}]
    thermostats = filter(lambda x: x['device_id'] == "thermostat", all_user_devices)
    door_sensors = filter(lambda x: x['device_id'] == "door_sensor", all_user_devices)
    motion_sensors = filter(lambda x: x['device_id'] == "motion_sensor", all_user_devices)
    light_switches = filter(lambda x: x['device_id'] == "light_switch", all_user_devices)
    return render_template("admin/admin_deviceactions.html", user=user, device=device, triggers=triggers, actors=actors,
                           thermostats=thermostats, light_switches=light_switches, door_sensors=door_sensors,
                           motion_sensors=motion_sensors, change_settings_form=form)


@admin_site.route('/user/<string:user_id>/device/<string:device_id>/configure', methods=['POST'])
def set_device_settings(user_id, device_id):
    form = SetThermostatTargetForm()
    if form.validate_on_submit():
        data_interface.set_thermostat_target(device_id, float(form.target_temperature.data))
        flash('Target temperature successfully set by Admin!', 'success')
        return redirect(url_for('.show_device', user_id=user_id, device_id=device_id))
    return show_device(device_id, form)


@admin_site.route('/user/<string:user_id>/device/<string:device_id>/switch/configure/<int:state>')
def set_switch_settings(user_id, device_id, state):
    error = data_interface.set_switch_state(device_id, state)
    if error is not None:
        flash("State successfully set by Admin", "success")
    return redirect(url_for('.show_device', user_id=user_id, device_id=device_id))

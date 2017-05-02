import logging

from flask import render_template, flash, redirect, url_for, request, jsonify

import data_interface
import shared.actions
import shared.triggers
from internal import internal_site
from shared.forms import SetThermostatTargetForm, CreateTriggerFormMotionSensor, \
    CreateTriggerFormThermostat, CreateTriggerActionFormThermostat
from shared.vendors import get_all_vendors_list, get_vendor_form, get_vendor_configuration_data, get_vendor_backend_id
from utilities.session import get_active_user


@internal_site.route('/devices')
def show_devices():
    all_vendors = get_all_vendors_list()
    devices = data_interface.get_user_devices(get_active_user()['user_id'])
    logging.info("devices: {}".format(devices))
    rooms = data_interface.get_user_default_rooms()
    rooms = sorted(rooms, key=lambda k: k['name'])
    any_linked = False
    any_unlinked = False
    moveinfo = []
    if devices:
        for device in devices:
            if device['room_id'] is not None:
                any_linked = True
            elif device['room_id'] is None:
                any_unlinked = True
    # change from default to focal user
    # test requires here to check if devices returns devices correctly
    return render_template("internal/devices.html", devices=devices, groupactions=shared.actions.groupactions,
                           rooms=rooms, all_vendors=all_vendors, table1=any_unlinked, table2=any_linked)


@internal_site.route('/devices/vendor/<string:vendor_id>/new', methods=['GET', 'POST'])
def add_new_device_for_vendor(vendor_id):
    form = get_vendor_form(vendor_id)
    if form.validate_on_submit():
        data_interface.add_new_device(user_id=get_active_user()['user_id'],
                                      device_type=form.device_type.data,
                                      vendor=get_vendor_backend_id(vendor_id),
                                      configuration=get_vendor_configuration_data(vendor_id, form),
                                      name=form.name.data)
        flash("New device successfully added!", 'success')
        return redirect(url_for('.show_devices'))
    return render_template("internal/new_device.html", new_device_form=form)


@internal_site.route('/device/<string:device_id>')
def show_device(device_id, thermostat_settings_form=None, create_trigger_form=None):
    device = data_interface.get_device_info(device_id)
    device_type = device['device_type']

    device_settings = None
    if device_type == "thermostat":
        device_settings = {"has_settings": True}
        if thermostat_settings_form is not None:
            device_settings["form"] = thermostat_settings_form
        else:
            device_settings["form"] = SetThermostatTargetForm()
    elif device_type == "light_switch":
        device_settings = {"has_settings": True}

    if create_trigger_form is not None:
        pass
    elif device_type == "thermostat":
        create_trigger_form = CreateTriggerFormThermostat(
            possible_affected_devices=data_interface.get_possible_affected_devices(device_id))
    elif device_type == "motion_sensor":
        create_trigger_form = CreateTriggerFormMotionSensor(
            possible_affected_devices=data_interface.get_possible_affected_devices(device_id))

    return render_template("internal/device_details.html",
                           device=device,
                           device_settings=device_settings,
                           affecting_triggers=data_interface.get_affecting_triggers(device_id),
                           affected_triggers=data_interface.get_affected_triggers(device_id),
                           create_trigger_form=create_trigger_form)


@internal_site.route('/device/<string:device_id>/triggers/create', methods=['POST'])
def create_trigger_for(device_id):
    device_info = data_interface.get_device_info(device_id)
    device_type = device_info["device_type"]
    if device_type == "thermostat":
        form = CreateTriggerFormThermostat(
            possible_affected_devices=data_interface.get_possible_affected_devices(device_id))
    elif device_type == "motion_sensor":
        form = CreateTriggerFormMotionSensor(
            possible_affected_devices=data_interface.get_possible_affected_devices(device_id))
    else:
        raise Exception()
    if form.validate_on_submit():
        actor_info = data_interface.get_device_info(form.affected_device.data)
        actor_type = actor_info["device_type"]
        if actor_type == "thermostat":
            action_form = CreateTriggerActionFormThermostat()
            action_form.event.data = form.event.data
            action_form.event_parameters.data = form.event_parameters.data
        else:
            raise Exception()
        return render_template("internal/triggers/create_trigger.html", device=device_info, actor=actor_info,
                               action_form=action_form)
    return show_device(device_id, create_trigger_form=form)


@internal_site.route('/device/<string:device_id>/triggers/create/actor/<string:actor_id>', methods=['POST'])
def create_trigger_action_for(device_id, actor_id):
    device_info = data_interface.get_device_info(device_id)
    device_type = device_info["device_type"]
    actor_info = data_interface.get_device_info(actor_id)
    actor_type = actor_info["device_type"]
    if actor_type == "thermostat":
        action_form = CreateTriggerActionFormThermostat()
    else:
        raise Exception()
    if not action_form.validate_on_submit():
        return create_trigger_for(device_id)
    result = data_interface.add_new_trigger(sensor_id=device_id,
                                            actor_id=actor_id,
                                            event=action_form.event.data,
                                            event_params=action_form.event_parameters.data,
                                            action=action_form.action.data,
                                            action_params=str(action_form.action_parameters.data),
                                            user_id=get_active_user()["user_id"])
    return redirect(url_for('.show_device', device_id=device_id))


@internal_site.route('/device/<string:device_id>/thermostat/configure', methods=['POST'])
def set_thermostat_settings(device_id):
    form = SetThermostatTargetForm()
    if form.validate_on_submit():
        data_interface.set_thermostat_target(device_id, float(form.target_temperature.data))
        flash('Target temperature successfully set!', 'success')
        return redirect(url_for('.show_device', device_id=device_id))
    return show_device(device_id, thermostat_settings_form=form)


@internal_site.route('/device/<string:device_id>/switch/configure/<int:state>')
def set_switch_settings(device_id, state):
    error = data_interface.set_switch_state(device_id, state)
    if error is not None:
        flash("State successfully set", "success")
    return redirect(url_for('.show_device', device_id=device_id))


@internal_site.route('/device/move', methods=['POST', 'GET'])
def move_device():
    device2room = request.form
    device2room = device2room.to_dict()
    data_interface.move_device2room(device2room)
    return jsonify(device2room)


@internal_site.route('/add_theme')
def add_theme():
    devices = data_interface.get_user_devices(get_active_user()['user_id'])
    rooms = data_interface.get_user_default_rooms()
    rooms = sorted(rooms, key=lambda k: k['name'])
    return render_template("internal/add_theme.html", devices=devices,
                           rooms=rooms)


@internal_site.route('/new_theme', methods=['POST', 'GET'])
def new_theme():
    theme_devices = request.form
    return 'done'


@internal_site.route('/themes')
def themes():
    themes = data_interface.get_user_themes(get_active_user()['user_id'])
    return render_template("internal/themes.html", themes=themes)


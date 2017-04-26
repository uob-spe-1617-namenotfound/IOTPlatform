from flask import render_template, flash, redirect, url_for

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
    rooms = data_interface.get_user_default_rooms()
    rooms = sorted(rooms, key=lambda k: k['name'])
    any_linked = False
    any_unlinked = False
    if devices:
        for device in devices:
            if device['room_id'] != None:
                any_linked = True
            elif device['room_id'] == None:
                any_unlinked = True
    # change from default to focal user
    # test requires here to check if devices returns devices correctly
    return render_template("internal/devices.html", devices=devices, groupactions=shared.actions.groupactions,
                           rooms=rooms, all_vendors=all_vendors, table1=any_unlinked, table2=any_linked)


@internal_site.route('/devices/vendor/<string:vendor_id>/new', methods=['GET', 'POST'])
def add_new_device(vendor_id=None):
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
def show_device(device_id, configuration_form=None, create_trigger_form=None):
    triggers = None
    device = data_interface.get_device_info(device_id)
    device_type = device['device_type']

    if configuration_form is not None:
        pass
    elif device_type == "thermostat":
        configuration_form = SetThermostatTargetForm()

    if create_trigger_form is not None:
        pass
    elif device_type == "thermostat":
        create_trigger_form = CreateTriggerFormThermostat(
            possible_affected_devices=data_interface.get_possible_affected_devices(device_id))
    elif device_type == "motion_sensor":
        create_trigger_form = CreateTriggerFormMotionSensor(
            possible_affected_devices=data_interface.get_possible_affected_devices(device_id))

    if device['device_type'] == "thermostat":
        triggers = shared.triggers.thermostat_triggers
        if configuration_form is None:
            configuration_form = SetThermostatTargetForm()
    elif device['device_type'] == "motion_sensor":
        triggers = shared.triggers.motion_triggers
    elif device['device_type'] == "light_switch":
        triggers = shared.triggers.light_triggers
    elif device['device_type'] == "door_sensor":
        triggers = shared.triggers.door_triggers
    all_user_devices = data_interface.get_user_devices(get_active_user()['user_id'])
    actors = [{"id": actor['device_id'], "name": actor['name'], "type": "device", "device": actor,
               "action": shared.actions.actions[actor['device_type']]} for actor in
              all_user_devices] + [{"id": "webhook_url", "type": "webhook", "url": "#", "name": "Send email"}]
    thermostats = filter(lambda x: x['device_id'] == "thermostat", all_user_devices)
    door_sensors = filter(lambda x: x['device_id'] == "door_sensor", all_user_devices)
    motion_sensors = filter(lambda x: x['device_id'] == "motion_sensor", all_user_devices)
    light_switches = filter(lambda x: x['device_id'] == "light_switch", all_user_devices)

    return render_template("internal/device_details.html",
                           device=device,
                           configuration_form=configuration_form,
                           affecting_triggers=data_interface.get_affecting_triggers(device_id),
                           affected_triggers=data_interface.get_affected_triggers(device_id),
                           create_trigger_form=create_trigger_form,
                           triggers=triggers, actors=actors,
                           thermostats=thermostats, light_switches=light_switches, door_sensors=door_sensors,
                           motion_sensors=motion_sensors)


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


@internal_site.route('/device/<string:device_id>/configure', methods=['POST'])
def set_device_settings(device_id):
    form = SetThermostatTargetForm()
    if form.validate_on_submit():
        data_interface.set_thermostat_target(device_id, float(form.target_temperature.data))
        flash('Target temperature successfully set!', 'success')
        return redirect(url_for('.show_device', device_id=device_id))
    return show_device(device_id, configuration_form=form)


@internal_site.route('/device/<string:device_id>/switch/configure/<int:state>')
def set_switch_settings(device_id, state):
    error = data_interface.set_switch_state(device_id, state)
    if error is not None:
        flash("State successfully set", "success")
    return redirect(url_for('.show_device', device_id=device_id))

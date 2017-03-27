from flask import redirect, url_for, flash, render_template

import data_interface
from admin import admin_site
from admin.views.admin_user_forms import AddNewRoomForm


@admin_site.route('/user/<string:user_id>')
def user(user_id):
    rooms = data_interface.get_default_rooms_for_user(user_id)
    user_info = data_interface.get_user_info(user_id)
    return render_template("admin/admin_user_home.html", admin=True, rooms=rooms, user_name=user_info["name"])


@admin_site.route('/room/add', methods=['POST', 'GET'])
def add_new_room():
    form = AddNewRoomForm()
    if form.validate_on_submit():
        try:
            data_interface.add_new_room(name=form.name.data)
        except Exception:
            flash("Error", "danger")
            return render_template("admin/admin_new_room.html", new_room_form=form)
        flash("New room successfully added!", 'success')
        return redirect(url_for('.user'))
    return render_template("admin/admin_new_room.html", new_room_form=form)



@admin_site.route('/room/<string:room_id>')
def view_room(room_id):
    room = data_interface.get_room_info(room_id)
    all_devices = data_interface.get_user_default_devices()
    print(all_devices)
    linked_devices = [d for d in all_devices if d['room_id'] is not None]
    unlinked_devices = [d for d in all_devices if d['room_id'] is None]
    room_devices = [d for d in all_devices if d['room_id'] == room_id]
    thermostats = [d for d in room_devices if d['device_type'] == "thermostat"]
    light_switches = [d for d in room_devices if d['device_type'] == "light_switch"]
    door_sensors = [d for d in room_devices if d['device_type'] == "door_sensor"]
    motion_sensors = [d for d in room_devices if d['device_type'] == "motion_sensor"]
    return render_template("admin/admin_roomview.html", room=room, thermostats=thermostats, light_switches=light_switches,
                           door_sensors=door_sensors, motion_sensors=motion_sensors, unlinked_devices=unlinked_devices,
                           linked_devices=linked_devices)


@admin_site.route('/room/<string:room_id>/device/<string:device_id>/link')
def link_device_to_room(room_id, device_id):
    data_interface.link_device_to_room(room_id, device_id)
    flash("Device was successfully linked by Admin!", "success")
    return redirect(url_for('.view_room', room_id=room_id))

from flask import render_template

import data_interface
from admin import admin_site


@admin_site.route('/user/<string:user_id>')
def user(user_id):
    rooms = data_interface.get_default_rooms_for_user(user_id)
    user_info = data_interface.get_user_info(user_id)
    return render_template("internal/home.html", admin=True, rooms=rooms, user_name=user_info["name"])


@admin_site.route('/faulty_devices', methods=['GET'])
def faulty_devices():
    faulty_devices = data_interface.get_faulty_devices()
    devices = []
    for d in faulty_devices:
        house = data_interface.get_house_info(d['house_id'])
        user = data_interface.get_user_info(house['user_id'])
        devices.append({"device": d, "user": user})
    return render_template("admin/faulty_devices.html", devices=devices)


@admin_site.route('/')
def index():
    users = data_interface.get_all_users()
    print(users)
    return render_template("admin/home.html", users=users)


@admin_site.route('/map')
def map():
    house1 = {'lat': 51.529249, 'lng': -0.117973}
    house2 = {'lat': 53.472605, 'lng': -2.227532}
    house3 = {'lat': 10.000, 'lng': 120.000}
    house_location = [house1, house2, house3]
    return render_template("admin/map.html", house_location=house_location)


@admin_site.route('/logout')
def logout():
    return "To be implemented"

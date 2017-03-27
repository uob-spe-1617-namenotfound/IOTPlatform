from flask import flash, redirect, url_for, render_template

import data_interface
import utilities.session
from admin import admin_site


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
    utilities.session.logout()
    flash('Successfully logged out', 'success')
    return redirect(url_for('public.index'))


@admin_site.route('/triggers')
def triggers():
    return render_template("admin/admin_triggers.html")


@admin_site.route('/help')
def help():
    return "admin help to be implemented"



@admin_site.route('/account/settings')
def account_settings():
    return "To be implemented"


status = ['Enabled', 'Disabled']
themeinfo = [{'id': '1', 'name': 'Weekend Away Theme', 'theme_status': status[0]},
             {'id': '2', 'name': 'Night Party Theme', 'theme_status': status[1]}]


@admin_site.route('/themes')
def themes():
    return render_template("admin/admin_themes.html", themeinfo=themeinfo, status=status)

@admin_site.route("/graph")
def graph():
    return render_template("admin/admin_user_graph.html")

from flask import flash, redirect, url_for, render_template

import data_interface
import utilities.session
from admin import admin_site
import itertools

@admin_site.route('/user/<string:user_id>')
def user(user_id):
    rooms = data_interface.get_default_rooms_for_user(user_id)
    user_info = data_interface.get_user_info(user_id)
    return render_template("internal/home.html", admin=True, rooms=rooms, user_name=user_info["name"])


@admin_site.route('/fault_status', methods=['GET'])
def fault_status():
    fault_status = data_interface.get_admin_fault_status()
    int_list = []
    for one_device in fault_status:
        int_list.append(one_device['faulty'])
    faults_list = [(k, len(list(v))) for k, v in itertools.groupby(sorted(int_list))]
    return render_template("admin/fault_status.html", faults_list = faults_list)


@admin_site.route('/')
def index():
    users = data_interface.get_all_users()
    for user in users:
        if user['faulty'] == False:
            user['faulty'] = str('OK')
        else:
            user['faulty'] = str('Faulty')
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

@admin_site.route('/maptest')
def maptest():
    house1 = {'lat': 51.529249, 'lng': -0.117973}
    house2 = {'lat': 53.472605, 'lng': -2.227532}
    house3 = {'lat': 10.000, 'lng': 120.000}
    house_location = [house1, house2, house3]
    return render_template("admin/maptest.html", house_location=house_location)

@admin_site.route('/test')
def test(r):
    return None
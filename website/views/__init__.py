from flask import render_template

from website import app

from website import data_interface

import website.views.devices
import website.views.rooms


@app.route('/triggers')
def triggers():
    return render_template("triggers.html")


@app.route('/')
def index():
    rooms = data_interface.get_user_default_rooms()
    return render_template("home.html", rooms=rooms)


@app.route('/admin/user/<string:user_id>')
def admin_index(user_id):
    rooms = data_interface.get_default_rooms_for_user(user_id)
    user_info = data_interface.get_user_info(user_id)
    return render_template("home.html", admin=True, rooms=rooms, user_name=user_info["name"])


@app.route('/logout')
def logout():
    return "To be implemented"


@app.route('/account/settings')
def account_settings():
    return "To be implemented"


@app.route('/admin')
def admin():
    users = data_interface.get_all_users()
    print(users)
    return render_template("admin.html", users=users)


@app.route('/admin_map')
def admin_map():
    house1 = {'lat': -20.000, 'lng': -179.000}
    house2 = {'lat': -50.000, 'lng': 45.000}
    house3 = {'lat': 10.000, 'lng': 120.000}
    house_location = [house1, house2, house3]
    return render_template("admin_maps.html", house_location=house_location)


@app.route('/help')
def help():
    return render_template("help.html")


status = ['Enabled', 'Disabled']
themeinfo = [{'id': '1', 'name': 'Weekend Away Theme', 'theme_status': status[0]},
             {'id': '2', 'name': 'Night Party Theme', 'theme_status': status[1]}]


@app.route('/themes')
def themes():
    return render_template("themes.html", themeinfo=themeinfo, status=status)

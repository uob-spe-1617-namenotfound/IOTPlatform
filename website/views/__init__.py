from flask import render_template

from website import app


@app.route('/triggers')
def triggers():
    return render_template("triggers.html")


@app.route('/')
def index():
    rooms = ['Kitchen', 'Bathroom']
    return render_template("home.html", rooms=rooms)


@app.route('/admin/user/<string:user_id>/<string:user_name>')
def admin_index(user_id, user_name):
    #user_name = user_repository.get_user(user_id).user_name
    rooms = ['Kitchen', 'Bathroom']
    return render_template("home.html", admin=True, rooms=rooms, user_name=user_name)


@app.route('/logout')
def logout():
    return "To be implemented"


@app.route('/account/settings')
def account_settings():
    return "To be implemented"


@app.route('/device/actions')
def device_actions():
    return render_template("deviceactions.html")


@app.route('/room')
def room_view():
    thermostatDict = {"Name": "Thermostat", "Property": "24℃", "Device_type" : "Thermostat"}

    lightSwitchDict1 = {"Name": "A", "Property": "On", "Device_type" : "Light Swtich"}
    lightSwitchDict2 = {"Name": "B", "Property": "On", "Device_type" : "Light Switch"}
    lightSwitchDict3 = {"Name": "C", "Property": "Off", "Device_type" : "Light Switch", "Device_type" : "Light Switch"}

    doorsensorDict1 = {"Name": "A", "Property": "4:20am", "Device_type" : "Close Sensor"}
    doorsensorDict2 = {"Name": "B", "Property": "2:40pm", "Device_type" : "Close Sensor"}
    doorsensorDict3 = {"Name": "C", "Property": "12:24pm", "Device_type" : "Close Sensor"}

    motionsensorDict1 = {"Name": "South Window", "Property": "Closed", "Device_type" : "Motion Sensor"}
    motionsensorDict2 = {"Name": "East Window", "Property": "Closed", "Device_type" : "Motion Sensor"}
    motionsensorDict3 = {"Name": "Door", "Property": "Open", "Device_type" : "Motion Sensor"}

    thermostats = [thermostatDict]
    light_switches = [lightSwitchDict1, lightSwitchDict2]
    door_sensors = [doorsensorDict1, doorsensorDict2, doorsensorDict3]
    motion_sensors = [motionsensorDict1, motionsensorDict2]

    unlinked_devices = [lightSwitchDict3, motionsensorDict3]
    linked_devices = [thermostats, light_switches, door_sensors, motion_sensors]
    return render_template("roomview.html", thermostats=thermostats, light_switches=light_switches,
                           door_sensors=door_sensors, motion_sensors=motion_sensors, unlinked_devices=unlinked_devices,
                           linked_devices=linked_devices)


@app.route('/devices')
def devices():
    return render_template("devices.html")


@app.route('/admin')
def admin():
    user_dic = {
        "user_id": "324123",
        "user_email_address": "wx15879@my.bristol.ac.uk",
        "user_is_admin": "Yes",
        "user_first_name": "Jack",
        "user_last_name": "Xia",
        "user_full_name": "Jack Xia",
        "user_device_status": "Fault"}
    userList = [user_dic]
    return render_template("admin.html", users=userList)

@app.route('/admin_map')
def admin_map():
    house1 = {'lat' : -20.000, 'lng': -179.000}
    house2 = {'lat' : -50.000, 'lng': 45.000}
    house3 = {'lat' :  10.000, 'lng': 120.000}
    house_location = [house1, house2, house3]
    return render_template("admin_maps.html", house_location = house_location)

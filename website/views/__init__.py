from flask import render_template

from website import app


@app.route('/triggers')
def triggers():
    return render_template("triggers.html")


@app.route('/')
def index():
    rooms = ['Kitchen', 'Bathroom']
    return render_template("home.html", rooms=rooms)


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
    thermostatDict = {"Name": "Thermostat", "Property": "24℃"}

    lightSwitchDict1 = {"Name": "A", "Property": "On"}
    lightSwitchDict2 = {"Name": "B", "Property": "On"}
    lightSwitchDict3 = {"Name": "C", "Property": "Off"}

    doorsensorDict1 = {"Name": "A", "Property": "4:20am"}
    doorsensorDict2 = {"Name": "B", "Property": "2:40pm"}
    doorsensorDict3 = {"Name": "C", "Property": "12:24pm"}

    motionsensorDict1 = {"Name": "South Window", "Property": "Closed"}
    motionsensorDict2 = {"Name": "East Window", "Property": "Closed"}
    motionsensorDict3 = {"Name": "Door", "Property": "Open"}

    thermostats = [thermostatDict]
    light_switches = [lightSwitchDict1, lightSwitchDict2, lightSwitchDict3]
    door_sensors = [doorsensorDict1, doorsensorDict2, doorsensorDict3]
    motion_sensors = [motionsensorDict1, motionsensorDict2, motionsensorDict3]

    return render_template("roomview.html", thermostats=thermostats, light_switches=light_switches,
                           door_sensors=door_sensors, motion_sensors=motion_sensors)


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
        "user_device_status": "Fault"}
    userList = [user_dic]
    return render_template("admin.html", users=userList)

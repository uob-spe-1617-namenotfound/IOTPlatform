from flask import render_template

from website import app

from website import data_interface

thermostatDict = {"Name": "Thermostat", "Property": "24℃", "Device_type": "Thermostat", "device_id": "10"}

lightSwitchDict1 = {"Name": "A", "Property": "On", "Device_type": "Light Swtich", "device_id": "11"}
lightSwitchDict2 = {"Name": "B", "Property": "On", "Device_type": "Light Switch", "device_id": "12"}
lightSwitchDict3 = {"Name": "C", "Property": "Off", "Device_type": "Light Switch", "device_id": "13"}

doorsensorDict1 = {"Name": "A", "Property": "4:20am", "Device_type": "Close Sensor", "device_id": "14"}
doorsensorDict2 = {"Name": "B", "Property": "2:40pm", "Device_type": "Close Sensor", "device_id": "15"}
doorsensorDict3 = {"Name": "C", "Property": "12:24pm", "Device_type": "Close Sensor", "device_id": "16"}

motionsensorDict1 = {"Name": "South Window", "Property": "Closed", "Device_type": "Motion Sensor", "device_id": "17"}
motionsensorDict2 = {"Name": "East Window", "Property": "Closed", "Device_type": "Motion Sensor", "device_id": "18"}
motionsensorDict3 = {"Name": "Door", "Property": "Open", "Device_type": "Motion Sensor", "device_id": "19"}

thermostats = [thermostatDict]
light_switches = [lightSwitchDict1, lightSwitchDict2]
door_sensors = [doorsensorDict1]
motion_sensors = [motionsensorDict1, motionsensorDict2]

unlinked_devices = [lightSwitchDict3, motionsensorDict3]
linked_devices = [thermostats, light_switches, door_sensors, motion_sensors]

deviceactions = [thermostatDict, lightSwitchDict1, lightSwitchDict2, doorsensorDict1, motionsensorDict1,
                 motionsensorDict2]
motionactions = ['Turn on', 'Turn Off', 'No Action']
lightactions = ['Turn Switch on', 'Turn Switch Off', 'No Action']
thermostatactions = ['Turn on', 'Turn Off', 'No Action', 'Modify Temperature']
actors = [{'id': '123', 'name': 'Motion Sensor', 'action': motionactions},
          {'name': 'Light Switch', 'id': '456', 'action': lightactions},
          {'name': 'Thermostat', 'id': '789', 'action': thermostatactions}]
motiontriggers = [{'id': '00', 'name': 'When Motion is Detected', 'trigactor': [actors]},
                  {'id': '01', 'name': 'When No Motion is Detected', 'trigactor': [actors]}]
thermostattriggers = [{'id': '000', 'name': 'When the temperature is above 22'},
                      {'id': '1111', 'name': 'When temperature is below 15'}]
lighttriggers = [
    {'id': '0000', 'name': 'Lights are on for 4 hours', 'trigactor': [actors], 'trigaction': [lightactions]}]

import website.views.devices
import website.views.rooms

@app.route('/triggers')
def triggers():
    return render_template("triggers.html")


@app.route('/')
def index():
    rooms = data_interface.get_user_default_rooms()
    return render_template("home.html", rooms=rooms)


@app.route('/admin/user/<string:user_id>/<string:user_name>')
def admin_index(user_id, user_name):
    rooms = ['Kitchen', 'Bathroom']
    return render_template("home.html", admin=True, rooms=rooms, user_name=user_name)


@app.route('/logout')
def logout():
    return "To be implemented"


@app.route('/account/settings')
def account_settings():
    return "To be implemented"


@app.route('/room')
def room_view():
    return render_template("roomview.html", thermostats=thermostats, light_switches=light_switches,
                           door_sensors=door_sensors, motion_sensors=motion_sensors, unlinked_devices=unlinked_devices,
                           linked_devices=linked_devices)




@app.route('/device/actions/')
def device_actions():
    triggers = None
    device = deviceactions[0]
    if device['Device_type'] == "Thermostat":
        triggers = thermostattriggers
    elif device['Device_type'] == "Motion Sensor":
        triggers = motiontriggers
    elif device['Device_type'] == "Light Switch":
        triggers = lighttriggers
    return render_template("deviceactions.html", device=deviceactions[0], triggers=triggers, actors=actors,
                           motionactions=motionactions, lightactions=lightactions,
                           thermostatactions=thermostatactions, thermostats=thermostats, light_switches=light_switches,
                           door_sensors=door_sensors, motion_sensors=motion_sensors, unlinked_devices=unlinked_devices,
                           linked_devices=linked_devices)


@app.route('/device/<string:device_id>')
def show_device(device_id):
    return "This is device {}".format(device_id)



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

@app.route('/help')
def help():
    return render_template("help.html")

status = ['Enabled', 'Disabled']
themeinfo = [{'id': '1', 'name': 'Weekend Away Theme', 'theme_status': status[0]},
             {'id': '2', 'name': 'Night Party Theme', 'theme_status': status[1]}]


@app.route('/themes')
def themes():
    return render_template("themes.html", themeinfo=themeinfo, status=status)
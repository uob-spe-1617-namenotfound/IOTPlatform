from flask import render_template

from website import app

rooms = ['Kitchen', 'Bathroom']


@app.route('/')
def index():
    return render_template("home.html", rooms=rooms)


@app.route('/logout')
def logout():
    return "To be implemented"


@app.route('/account/settings')
def account_settings():
    return "To be implemented"


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


@app.route('/room')
def room_view():
    return render_template("roomview.html", thermostats=thermostats, light_switches=light_switches,
                           door_sensors=door_sensors, motion_sensors=motion_sensors, unlinked_devices=unlinked_devices,
                           linked_devices=linked_devices)


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


paireddevices = [
    {'text': 'Bathroom Thermostat', 'device_id': '10', 'type': 'thermostat', 'trigger': thermostattriggers},
    {'text': 'Kitchen Thermostat', 'device_id': '20', 'type': 'thermostat', 'trigger': thermostattriggers},
    {'text': 'Dining Room Thermostat', 'device_id': '30', 'type': 'thermostat', 'trigger': thermostattriggers},
    {'text': 'Dining Room Motion Sensor', 'id': '40', 'type': 'motion_sensor', 'trigger': motiontriggers},
    {'text': 'Bedroom Motion Sensor', 'id': '50', 'type': 'motion_sensor', 'trigger': motiontriggers},
    {'text': 'Bathroom Light Switch', 'id': '60', 'type': 'light_switch', 'trigger': lighttriggers}]

groupactions = ['Turn On', 'Turn Off', 'Set Temperature']
groups = [{'id': '11', 'name': 'Ground Floor Thermostats', 'device_ids': [paireddevices[1], paireddevices[2]],
           'group_actions': [groupactions[0], groupactions[1], groupactions[2]]},
          {'id': '21', 'name': 'Motion In Bedrooms', 'device_ids': [paireddevices[3]],
           'group_actions': [groupactions[0], groupactions[1]]},
          {'id': '31', 'name': 'Lighting in First Floor', 'device_ids': [paireddevices[4]],
           'group_actions': [groupactions[0], groupactions[1]]}]


@app.route('/devices')
def devices():
    return render_template("devices.html", paireddevices=paireddevices, groups=groups, groupactions=groupactions)


@app.route('/help')
def help():
    return render_template("help.html")


status = ['Enabled', 'Disabled']
themeinfo = [{'id': '1', 'name': 'Weekend Away Theme', 'theme_status': status[0]},
             {'id': '2', 'name': 'Night Party Theme', 'theme_status': status[1]}]


@app.route('/themes')
def themes():
    return render_template("themes.html", themeinfo=themeinfo, status=status)

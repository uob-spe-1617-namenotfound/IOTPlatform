from flask import render_template

from website import app


@app.route('/triggers')
def triggers():
    return render_template("triggers.html")


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


paireddevices = [{'text': 'Bathroom Thermostat', 'id': '10', 'type': 'thermostat'},
                 {'text': 'Kitchen Thermostat', 'id': '20', 'type': 'thermostat'},
                 {'text': 'Dining Room Thermostat', 'id': '30', 'type': 'thermostat'},
                 {'text': 'Dining Room Motion Sensor', 'id': '40', 'type': 'motion_sensor'},
                 {'text': 'Bedroom Motion Sensor', 'id': '50', 'type': 'motion_sensor'},
                 {'text': 'Bathroom Light Switch', 'id': '60', 'type': 'light_switch'}]

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


@app.route('/device/actions')
def device_actions():
    return render_template("deviceactions.html", device=paireddevices[3], triggers=motiontriggers, actors=actors,
                           motionactions=motionactions, lightactions=lightactions,
                           thermostatactions=thermostatactions)


class Devices:
    def __init__(self, type, devices, property):
        self.type = type
        self.devices = devices
        self.property = property


dev1 = Devices("Thermostat", ["Thermostat"], "24℃")
dev2 = Devices("Door & Window Sensor", ["South Window", "East Window", 'Door'], ['Closed', 'Closed', 'Open'])
device = [dev1, dev2]

@app.route('/room')
def room_view():
    return render_template("roomview.html", device=device)


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


@app.route('/device/<string:id>')
def show_device(id):
    return "This is device {}".format(id)

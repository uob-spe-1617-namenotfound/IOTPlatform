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


triggers = ["When Motion is Detected", "When No Motion is Detected"]
actors = ["Light Switch", "Thermostat", "Motion Sensor"]
@app.route('/device/actions')
def device_actions():
    return render_template("deviceactions.html", triggers=triggers, actors=actors)


class Devices:
    def __init__(self, type, devices, property):
        self.type = type
        self.devices = devices
        self.property = property


dev1 = Devices("Thermostat", ["Thermostat"], "24℃")
dev2 = Devices("Door & Window Sensor", ["South Window", "East Window", 'Door'], ['Closed', 'Closed', 'Open'])
devices = [dev1, dev2]

@app.route('/room')
def room_view():
    return render_template("roomview.html", devices=devices)


paireddevices = [{'text': 'Bathroom Thermostat'}, {'text': 'Kitchen Thermostat'}, {'text': 'Bedroom Thermostat'},
                 {'text': 'Dining Room Motion Sensor'}, {'text': 'Bedroom Motion Sensor'},
                 {'text': 'Bathroom Window/door sensor'}]
group = ["Ground Floor thermostats"]
devicename = ["Kitchen Thermostat", "Living Room Thermostat", "Dining Room Thermostat"]
@app.route('/devices')
def devices():
    return render_template("devices.html", paireddevices=paireddevices, group=group, devicename=devicename)


@app.route('/help')
def help():
    return render_template("help.html")


themes = ["Weekend Away", "Night Party Theme"]


@app.route('/themes')
def themes():
    return render_template("themes.html", themes=themes)

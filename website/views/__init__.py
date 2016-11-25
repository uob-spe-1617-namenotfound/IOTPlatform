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


@app.route('/device/actions')
def device_actions():
    return render_template("deviceactions.html")

class Devices:
    def __init__(self, type, devices, property):
        self.type = type
        self.devices = devices
        self.property = property


dev1 = Devices("Thermostat", ["Thermostat"], "24℃")
dev2 = Devices("Door & Window Sensor", ["South Window","East Window", 'Door'], ['Closed', 'Closed', 'Open'])
devices = [dev1, dev2]

@app.route('/room')
def room_view():
    return render_template("roomview.html", devices=devices)


@app.route('/devices')
def devices():
    return render_template("devices.html")


@app.route('/help')
def help():
    return render_template("help.html")


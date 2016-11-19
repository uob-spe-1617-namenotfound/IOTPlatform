from flask import render_template

from website import app


@app.route('/triggers')
def triggers():
    return render_template("triggers.html")


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/logout')
def logout():
    return "To be implemented"


@app.route('/account/settings')
def account_settings():
    return "To be implemented"


@app.route('/home/actions')
def home_actions():
    return render_template("homeactions.html")


@app.route('/room')
def room_view():
    return render_template("roomview.html")


@app.route('/devices')
def devices():
    return render_template("devices.html")

@app.route('/help')
def help():
    return render_template("help.html")
from flask import render_template

from website import app

@app.route('/Triggers')
def triggers():
        return render_template("Triggers.html")

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/logout')
def logout():
    return "To be implemented"


@app.route('/account/settings')
def account_settings():
    return "To be implemented"

@app.route('/Home Actions')
def home_actions():
    return render_template("homeactions.html")

@app.route('/Room View')
def room_view():
    return render_template("roomview.html")

@app.route('/Devices')
def devices():
    return render_template("Devices.html")

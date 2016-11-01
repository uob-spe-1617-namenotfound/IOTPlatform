from flask import render_template

from website import app


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/logout')
def logout():
    return "To be implemented"


@app.route('/account/settings')
def account_settings():
    return "To be implemented"

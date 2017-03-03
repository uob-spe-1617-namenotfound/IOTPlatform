from flask import render_template

from public import public_site


@public_site.route('/')
@public_site.route('/index')
@public_site.route('/home')
def index():
    return render_template('public/home.html')


@public_site.route('/help')
def help():
    return render_template('public/help.html')


@public_site.route('/register')
def register():
    return "Not implemented yet"


@public_site.route('/login')
def login():
    return "Not implemented yet"

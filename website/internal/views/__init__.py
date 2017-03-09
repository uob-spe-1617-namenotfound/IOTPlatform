from flask import render_template, redirect, flash, url_for

import data_interface
from internal import internal_site
from internal.views import rooms, devices

import utilities.session
@internal_site.route('/triggers')
def triggers():
    return render_template("internal/triggers.html")


@internal_site.route('/')
def index():
    rooms = data_interface.get_user_default_rooms()
    return render_template("internal/home.html", rooms=rooms)


@internal_site.route('/help')
def help():
    return "Internal help to be implemented"


@internal_site.route('/logout')
def logout():
    utilities.session.logout()
    flash('Successfully logged out', 'success')
    return redirect(url_for('public.index'))


@internal_site.route('/account/settings')
def account_settings():
    return "To be implemented"


status = ['Enabled', 'Disabled']
themeinfo = [{'id': '1', 'name': 'Weekend Away Theme', 'theme_status': status[0]},
             {'id': '2', 'name': 'Night Party Theme', 'theme_status': status[1]}]


@internal_site.route('/themes')
def themes():
    return render_template("internal/themes.html", themeinfo=themeinfo, status=status)

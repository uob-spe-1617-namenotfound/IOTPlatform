import csv
import logging
from io import StringIO

from flask import render_template, redirect, flash, url_for, make_response

import data_interface
import utilities.session
from internal import internal_site
from internal.views import rooms, devices
from internal.views.forms import AddNewRoomForm


@internal_site.route('/triggers')
def triggers():
    return render_template("internal/triggers.html")


@internal_site.route('/')
def index():
    form = AddNewRoomForm()
    rooms = data_interface.get_user_default_rooms()
    return render_template("internal/home.html", rooms=rooms, new_room_form=form)


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


@internal_site.route("/graph")
def graph():
    return render_template("internal/graph.html")


@internal_site.route('/graph/data')
def graph_data():
    si = StringIO()
    cw = csv.writer(si)
    data = data_interface.get_user_graph_data(utilities.session.get_active_user()['user_id'])
    cw.writerow(["date", "close"])
    keys = sorted(data.keys())
    for k in keys:
        cw.writerow([k, data[k]])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@internal_site.route('/graph_test')
def graph_test():
    return render_template("internal/graph_test.html")

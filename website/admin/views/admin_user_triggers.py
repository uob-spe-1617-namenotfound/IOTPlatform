from flask import render_template

import data_interface
from admin import admin_site

motion_triggers = [{'id': '00', 'name': 'When Motion is Detected'},
                   {'id': '01', 'name': 'When No Motion is Detected'}]
thermostat_triggers = [{'id': '000', 'name': 'When the temperature is above 22'},
                       {'id': '1111', 'name': 'When temperature is below 15'}]
light_triggers = [{'id': '0000', 'name': 'Lights are on for 4 hours'}]
door_triggers = [{'id': 'opens', 'name': "Opens"}, {'id': 'closes', 'name': "Closes"}]


groupactions = ['Turn On', 'Turn Off', 'Set Temperature']

actions = {"door_sensor": ['Turn on', 'Turn Off', 'No Action'],
           "light_switch": ['Turn Switch on', 'Turn Switch Off', 'No Action'],
           "thermostat": ['Turn on', 'Turn Off', 'No Action', 'Modify Temperature'],
           "motion_sensor": ['Turn on', 'Turn Off', 'No Action']}


@admin_site.route('/user/<string:user_id>/themes')
def themes():
    return render_template("admin/admin_themes.html", themeinfo=themeinfo, status=status)


@admin_site.route('/user/<string:user_id>/triggers')
def triggers():
    return render_template("admin/admin_triggers.html")

@admin_site.route("/graph")
def graph():
    return render_template("admin/admin_user_graph.html")


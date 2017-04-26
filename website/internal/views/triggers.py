from flask import render_template, redirect, url_for, flash

import data_interface
from internal import internal_site
from utilities.session import get_active_user


@internal_site.route('/triggers')
def show_all_triggers():
    all_triggers = data_interface.get_triggers_for_user(get_active_user()["user_id"])
    return render_template("internal/triggers/all_triggers.html", all_triggers=all_triggers)


@internal_site.route('/trigger/<string:trigger_id>/delete')
def delete_trigger(trigger_id):
    data_interface.remove_trigger(trigger_id)
    flash("Trigger successfully removed", "success")
    return redirect(url_for('.show_all_triggers'))

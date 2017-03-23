from flask import render_template, redirect, url_for, flash

import data_interface.users
import utilities.session
from public import public_site
from public.views.forms import RegisterForm, LoginForm
import logging


@public_site.route('/')
@public_site.route('/index')
@public_site.route('/home')
def index():
    return render_template('public/home.html')


@public_site.route('/help')
def help():
    return render_template('public/help.html')


@public_site.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result, error = data_interface.users.register_user(
            email_address=form.email_address.data,
            password=form.password.data,
            name=form.name.data
        )
        if error is None:
            flash('Successfully registered', 'success')
            return redirect(url_for('.login'))
        flash(str(error), 'danger')
    return render_template('public/register.html', register_form=form)


@public_site.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        logging.debug("Form validated!")
        result, error = data_interface.users.login(
            email_address=form.email_address.data,
            password=form.password.data
        )
        logging.debug("data interface login result: {} {}".format(result, error))
        if error is None:
            error = utilities.session.login(result['user_id'], result['token'], result['admin'])
        if error is None:
            flash('Successfully logged in', 'success')
            return redirect(url_for('internal.index'))
        flash(str(error), 'danger')
    return render_template('public/login.html', login_form=form)

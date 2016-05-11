from flask import render_template, request, url_for, flash, redirect, session
import flask
from flask.ext.login import login_required
from flask.ext.login import login_user
from . import app
from .models import User
from .forms import LoginForm
from .confirmation_sender import send_confirmation_code


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/secret-page')
@login_required
def secret_page():
    return ''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if user.password_valid(form.password.data.encode('utf8')):
                session['user_email'] = user.email
                return redirect(url_for('confirmation'))
        flash('Wrong user/password.', 'error')
    return render_template('login.html', form=form)


@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    user_id = session.get('user_email', None)
    if not user_id:
        flask.abort(401)
    user = User.query.get(user_id)
    if request.method == 'POST':
        given_code = request.form['verification_code']
        if given_code == session['confirmation_code']:
            login_user(user)
            return redirect(url_for('secret_page'))
    code = send_confirmation_code(user.international_phone_number)
    session['confirmation_code'] = code
    return render_template('confirmation.html', user=user)

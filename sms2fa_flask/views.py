from flask import render_template, request, url_for, flash, redirect, session
import flask
from flask.ext.login import login_required
from flask.ext.login import login_user
from . import app
from .models import User


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/secret-page')
@login_required
def secret_page():
    return ''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = User.query.get(request.form['email'])
    given_password = request.form['password'].encode('utf8')
    if not user or not user.password_valid(given_password):
        flash('Wrong user/password.', 'error')
        return render_template('login.html')
    session['user_id'] = user.email
    return redirect(url_for('confirmation'))


@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    user_id = session.get('user_id', None)
    if not user_id:
        flask.abort(401)
    if request.method == 'GET':
        session['confirmation_code'] = '1234'
    return render_template('confirmation.html')

from flask import render_template, request, url_for, flash, redirect
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
    login_user(user)
    return redirect(url_for('confirmation'))


@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    return render_template('confirmation.html')

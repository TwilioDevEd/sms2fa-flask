from flask import render_template, request, url_for
from flask.ext.login import login_required
from . import app


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/secret-page')
@login_required
def secret_page():
    return ''

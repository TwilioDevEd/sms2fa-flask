from flask import render_template, jsonify, request, url_for


def routes(app):
    app.route('/')(root)


def root():
    return render_template('index.html')

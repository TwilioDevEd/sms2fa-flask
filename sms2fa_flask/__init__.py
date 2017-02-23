from sms2fa_flask.config import config_env_files
from sms2fa_flask.models import db, User
from flask import Flask

from flask.ext.login import LoginManager
from flask.ext.session import Session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
login_manager = LoginManager()
sess = Session()


def prepare_app(environment='development', p_db=db):
    app.config.from_object(config_env_files[environment])
    login_manager.setup_app(app)
    p_db.init_app(app)
    sess.init_app(app)
    app.session_interface.db.create_all()
    from . import views
    return app


def save_and_commit(item):
    db.session.add(item)
    db.session.commit()
db.save = save_and_commit


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

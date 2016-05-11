from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
import bcrypt
import phonenumbers
from phonenumbers import PhoneNumberFormat
db = SQLAlchemy()


class User(db.Model, UserMixin):

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    active = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=False)

    def password_valid(self, pwd):
        pwd_hash = self.password.decode('utf8').encode('utf8')
        return bcrypt.hashpw(pwd, pwd_hash) == pwd_hash

    # The methods below are required by flask-login
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    @property
    def international_phone_number(self):
        parsed_number = phonenumbers.parse(self.phone_number)
        return phonenumbers.format_number(parsed_number,
                                          PhoneNumberFormat.INTERNATIONAL)

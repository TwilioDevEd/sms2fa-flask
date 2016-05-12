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

    @classmethod
    def save_from_dict(cls, data):
        user = User(**data)
        user.set_password(data['password'])
        user.active = False
        db.save(user)
        return user

    def password_valid(self, pwd):
        pwd_hash = self.password.decode('utf8').encode('utf8')
        return bcrypt.hashpw(pwd, pwd_hash) == pwd_hash

    def set_password(self, new_password):
        new_password = new_password.encode('utf8')
        hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())
        self.password = hashed_password

    @property
    def international_phone_number(self):
        parsed_number = phonenumbers.parse(self.phone_number)
        return phonenumbers.format_number(parsed_number,
                                          PhoneNumberFormat.INTERNATIONAL)

    # The methods below are required by flask-login
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

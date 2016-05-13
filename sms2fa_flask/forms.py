from flask_wtf import Form
from wtforms import TextField, PasswordField, validators
from flask_wtf.html5 import TelField, EmailField
from wtforms.validators import DataRequired
import phonenumbers


class LoginForm(Form):
    email = TextField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SignUpForm(Form):
    first_name = TextField('first name', validators=[DataRequired()])
    last_name = TextField('last name', validators=[DataRequired()])
    phone_number = TelField('phone number', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', [validators.Required(),
                             validators.EqualTo('confirm',
                             message='Passwords must match')])
    confirm = PasswordField('confirm password', [validators.Required()])

    def validate_phone_number(self, field):
        error_message = "Invalid phone number. Example: +5599999999"
        try:
            data = phonenumbers.parse(field.data)
        except:
            raise validators.ValidationError(error_message)
        if not phonenumbers.is_possible_number(data):
            raise validators.ValidationError(error_message)

    @property
    def as_dict(self):
        data = self.data
        del data['confirm']
        return data

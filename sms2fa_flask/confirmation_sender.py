from twilio.rest import TwilioRestClient
from . import app
import random


def send_confirmation_code(to_number):
    code = generate_code()
    account_sid = app.config['TWILIO_ACCOUNT_SID']
    auth_token = app.config['TWILIO_AUTH_TOKEN']
    twilio_number = app.config['TWILIO_NUMBER']
    client = TwilioRestClient(account_sid, auth_token)
    client.messages.create(to=to_number,
                           from_=twilio_number,
                           body=code)
    return code


def generate_code():
    return str(random.randrange(100000, 999999))

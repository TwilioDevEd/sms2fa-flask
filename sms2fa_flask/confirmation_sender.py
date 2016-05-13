from twilio.rest import TwilioRestClient
from . import app
from flask import session
import random


def send_confirmation_code(to_number):
    code = generate_code()
    send_sms(to_number, code)
    session['confirmation_code'] = code
    return code


def generate_code():
    return str(random.randrange(100000, 999999))


def send_sms(to_number, body):
    account_sid = app.config['TWILIO_ACCOUNT_SID']
    auth_token = app.config['TWILIO_AUTH_TOKEN']
    twilio_number = app.config['TWILIO_NUMBER']
    client = TwilioRestClient(account_sid, auth_token)
    client.messages.create(to=to_number,
                           from_=twilio_number,
                           body=body)

from .base import BaseTest
from flask import session
from sms2fa_flask import confirmation_sender
from mock import patch
from mock import MagicMock


class ConfirmationSenderTest(BaseTest):

    def test_sender_creates_a_message(self):
        confirmation_sender.generate_code = MagicMock(return_value='random_code')
        with patch('twilio.rest.resources.messages.Messages.create') as create_mock:
            confirmation_sender.send_confirmation_code('+15551234321')
            create_mock.assert_called_once_with(
                    body='random_code',
                    from_=self.app.config['TWILIO_NUMBER'],
                    to=u'+15551234321'
            )
            self.assertEquals('random_code', session.get('verification_code'))

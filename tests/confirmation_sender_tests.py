from .base import BaseTest
from sms2fa_flask.confirmation_sender import send_confirmation_code
import six
if six.PY3:
    from unittest.mock import patch
else:
    from mock import patch


class ConfirmationSenderTest(BaseTest):

    def test_sender_creates_a_message(self):
        with patch('twilio.rest.resources.messages.Messages.create') as create_mock:
            send_confirmation_code('+15551234321', code='123')
            create_mock.assert_called_once_with(
                    body='123',
                    from_=self.app.config['TWILIO_NUMBER'],
                    to=u'+15551234321'
            )

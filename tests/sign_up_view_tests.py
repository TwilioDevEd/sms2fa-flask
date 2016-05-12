from .base import BaseTest
from flask import url_for, session
from flask.ext.login import current_user
import six
from sms2fa_flask.models import User
if six.PY3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


class SignUpTest(BaseTest):

    def test_sign_up_success_creates_user(self):
        data = {'email': '00@7.com',
                'password': self.password,
                'confirm': self.password,
                'first_name': 'James',
                'last_name': "O'Seven",
                'phone_number': "+5599999007",
                'password': self.password}
        response = self.client.post(url_for('sign_up'), data=data)
        self.assertEquals(302, response.status_code)
        user = User.query.get(data['email'])
        self.assertTrue(user)
        self.assertTrue(user.password_valid(data['password']))

    def test_sign_up_success_redirects(self):
        data = {'email': '00@7.com',
                'password': self.password,
                'confirm': self.password,
                'first_name': 'James',
                'last_name': "O'Seven",
                'phone_number': "+5599999007",
                'password': self.password}
        response = self.client.post(url_for('sign_up'), data=data)
        self.assertEquals(302, response.status_code)
        expected_path = url_for('confirmation')
        self.assertIn(expected_path, urlparse(response.location).path)

    def test_sign_up_success_puts_user_email_in_session(self):
        data = {'email': '00@7.com',
                'password': self.password,
                'confirm': self.password,
                'first_name': 'James',
                'last_name': "O'Seven",
                'phone_number': "+5599999007",
                'password': self.password}
        with self.app.test_client() as client:
            response = client.post(url_for('sign_up'), data=data)
            self.assertEquals(302, response.status_code)
            self.assertIn('user_email', session)
            self.assertEquals(data['email'], session['user_email'])
            self.assertFalse(current_user.is_authenticated)

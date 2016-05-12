from .base import BaseTest
from flask import url_for, session
from flask.ext.login import current_user
import six
if six.PY3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


class SignInTest(BaseTest):

    def test_sign_in_success_redirects(self):
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(url_for('sign_in'), data=data)
        self.assertEquals(302, response.status_code)
        expected_path = url_for('confirmation')
        self.assertIn(expected_path, urlparse(response.location).path)

    def test_sign_in_success_puts_user_email_in_session(self):
        data = {'email': self.email, 'password': self.password}
        with self.app.test_client() as client:
            client.post(url_for('sign_in'), data=data)
            self.assertIn('user_email', session)
            self.assertEquals(self.email, session['user_email'])
            self.assertFalse(current_user.is_authenticated)

    def test_sign_in_failure(self):
        data = {'email': self.email, 'password': 'I am a hacker'}
        with self.app.test_client() as client:
            response = client.post(url_for('sign_in'), data=data)
            self.assertEquals(200, response.status_code)
            self.assertIn('Welcome back', response.data.decode('utf8'))
            self.assertIn('Wrong user/password.', response.data.decode('utf8'))
            self.assertNotIn('user_email', session)
            self.assertFalse(current_user.is_authenticated)

    def test_logout_kills_session(self):
        with self.app.test_client() as client:
            with client.session_transaction() as current_session:
                current_session['user_email'] = self.email
                current_session['confirmation_code'] = '1234'
            response = client.get(url_for('logout'))
            self.assertNotIn('confirmation_code', session)
            self.assertNotIn('user_email', session)
        self.assertEquals(302, response.status_code)
        expected_path = url_for('root')
        self.assertIn(expected_path, urlparse(response.location).path)
        self.assertFalse(current_user.is_authenticated)

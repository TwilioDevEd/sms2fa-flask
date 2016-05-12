from .base import BaseTest
from flask import url_for, session
from flask.ext.login import current_user
import six
from mock import MagicMock
from sms2fa_flask import views
from sms2fa_flask.models import User
if six.PY3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


class RootTest(BaseTest):

    def test_root(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)
        self.assertIn('can be tricky', response.data.decode('utf8'))

    def test_secret_page_without_auth(self):
        response = self.client.get('/secret-page')
        self.assertEquals(401, response.status_code)

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

    def test_confirmation_page_fails_for_strangers(self):
        response = self.client.get(url_for('confirmation'))
        self.assertEquals(401, response.status_code)

    def test_confirmation_page_puts_confirmation_code_on_session(self):
        views.send_confirmation_code = MagicMock(return_value='random_code')
        with self.app.test_client() as client:
            with client.session_transaction() as current_session:
                current_session['user_email'] = self.email
            response = client.get(url_for('confirmation'))
            self.assertEquals(200, response.status_code)
            self.assertIn('confirmation_code', session)
            self.assertEquals('random_code', session['confirmation_code'])

    def test_confirmation_page_shows_current_phone(self):
        views.send_confirmation_code = MagicMock(return_value='1234')
        with self.app.test_client() as client:
            with client.session_transaction() as current_session:
                current_session['user_email'] = self.email
            response = client.get(url_for('confirmation'))
        self.assertEquals(200, response.status_code)
        self.assertIn(self.default_user.international_phone_number,
                      response.data.decode('utf8'))

    def test_confirmation_page_authenticates_on_success(self):
        with self.app.test_client() as client:
            with client.session_transaction() as current_session:
                current_session['user_email'] = self.email
                current_session['confirmation_code'] = '1234'
            client.post(url_for('confirmation'),
                        data={'verification_code': '1234'})
            self.assertTrue(current_user.is_authenticated)

    def test_confirmation_page_doesnt_authenticates_on_failure(self):
        views.send_confirmation_code = MagicMock(return_value='1234')
        with self.app.test_client() as client:
            with client.session_transaction() as current_session:
                current_session['user_email'] = self.email
                current_session['confirmation_code'] = '1234'
            client.post(url_for('confirmation'),
                        data={'verification_code': 'wrong_one'})
            self.assertFalse(current_user.is_authenticated)

    def test_confirmation_page_redirect_to_secrets_page_on_success(self):
        with self.app.test_client() as client:
            with client.session_transaction() as current_session:
                current_session['user_email'] = self.email
                current_session['confirmation_code'] = '1234'
            response = client.post(url_for('confirmation'),
                                   data={'verification_code': '1234'})
        self.assertEquals(302, response.status_code)
        expected_path = url_for('secret_page')
        self.assertIn(expected_path, urlparse(response.location).path)

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

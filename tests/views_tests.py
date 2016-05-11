from .base import BaseTest
from flask import url_for, session
from flask.ext.login import current_user
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse


class RootTest(BaseTest):

    def test_root(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)
        self.assertIn('can be tricky', response.data.decode('utf8'))

    def test_secret_page_without_auth(self):
        response = self.client.get('/secret-page')
        self.assertEquals(401, response.status_code)

    def test_login_success_redirects(self):
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(url_for('login'), data=data)
        self.assertEquals(302, response.status_code)
        expected_path = url_for('confirmation')
        self.assertIn(expected_path, urlparse(response.location).path)

    def test_login_success_puts_user_id_in_session(self):
        data = {'email': self.email, 'password': self.password}
        with self.app.test_client() as client:
            client.post(url_for('login'), data=data)
            self.assertFalse(current_user.is_authenticated())
            self.assertIn('user_id', session)
            self.assertEquals(self.email, session['user_id'])

    def test_login_failure(self):
        data = {'email': self.email, 'password': 'I am a hacker'}
        with self.app.test_client() as client:
            response = client.post(url_for('login'), data=data)
            self.assertEquals(200, response.status_code)
            self.assertIn('Welcome back', response.data.decode('utf8'))
            self.assertIn('Wrong user/password.', response.data.decode('utf8'))
            self.assertNotIn('user_id', session)
            self.assertFalse(current_user.is_authenticated)

    def test_confirmation_page_fails_for_strangers(self):
        response = self.client.get(url_for('confirmation'))
        self.assertEquals(401, response.status_code)

    def test_confirmation_page_puts_confirmation_code_on_session(self):
        with self.app.test_client() as client:
            with client.session_transaction() as current_session:
                current_session['user_id'] = self.email
            response = client.get(url_for('confirmation'))
            self.assertEquals(200, response.status_code)
            self.assertIn('confirmation_code', session)

from .base import BaseTest
from flask import url_for
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

    def test_login_success(self):
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(url_for('login'), data=data)
        self.assertEquals(302, response.status_code)
        expected_path = url_for('confirmation')
        self.assertIn(expected_path, urlparse(response.location).path)

    def test_login_failure(self):
        data = {'email': self.email, 'password': 'I am a hacker'}
        response = self.client.post(url_for('login'), data=data)
        self.assertEquals(200, response.status_code)
        self.assertIn('Welcome back', response.data.decode('utf8'))
        self.assertIn('Wrong user/password.', response.data.decode('utf8'))

from .base import BaseTest
from mock import Mock
import json
from flask import url_for
from sms2fa_flask import views


class RootTest(BaseTest):

    def test_root(self):
        response = self.client.get('/')

        self.assertEquals(200, response.status_code)

    def test_secret_page_without_auth(self):
        response = self.client.get('/secret-page')

        self.assertEquals(401, response.status_code)

from .base import BaseTest
from mock import Mock
import json
from flask import url_for
from sms2fa_flask import views


class RootTest(BaseTest):

    def test_renders_all_questions(self):
        response = self.client.get('/')

        self.assertEquals(200, response.status_code)

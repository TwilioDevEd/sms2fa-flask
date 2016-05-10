from xmlunittest import XmlTestCase
from sms2fa_flask.models import User


class BaseTest(XmlTestCase):

    def setUp(self):
        from sms2fa_flask import app, db
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.db = db
        self.client = self.app.test_client()
        User.query.delete()
        self.default_user = User(email="example@example.com")
        db.save(self.default_user)

from xmlunittest import XmlTestCase
from sms2fa_flask.models import User
import bcrypt


class BaseTest(XmlTestCase):

    def setUp(self):
        from sms2fa_flask import app, db
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.db = db
        self.client = self.app.test_client()
        User.query.delete()
        self.password = '1234'.encode('utf8')
        pwd_hash = bcrypt.hashpw(self.password, bcrypt.gensalt())
        self.default_user = User(email="example@example.com",
                                 password=pwd_hash)
        db.save(self.default_user)

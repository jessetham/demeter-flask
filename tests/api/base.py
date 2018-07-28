import unittest
from app import create_app, db
from config import UnitTestConfig

class BaseAPICase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(UnitTestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

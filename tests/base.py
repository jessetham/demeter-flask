import unittest
from app import create_app, db
from config import UnitTestConfig
from tests import utl

class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(UnitTestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        utl.init()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

import unittest
from app import create_app, db
from config import UnitTestConfig
from tests import utl

class SensorsAPICase(unittest.TestCase):
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

    def test_create(self):
        utl.add_categories_to_db(self)
        for sensor in utl.SENSORS:
            res = self.client.post('/api/sensors',
                json={
                    'name': sensor['name'],
                    'categories': sensor['categories']
            })
            self.assertEqual(res.status_code, 201, res.get_json())

    def test_get_single(self):
        utl.add_categories_to_db(self)
        utl.add_sensors_to_db(self)
        # Get a sensor that hasn't been created yet
        res = self.client.get('/api/sensors/42')
        self.assertEqual(res.status_code, 404, res.get_json())

        # Get a sensor that has been created
        res = self.client.get('/api/sensors/1')
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_get_multiple(self):
        utl.add_categories_to_db(self)
        utl.add_sensors_to_db(self)

        # Get the list of sensor stored in the db
        res = self.client.get('/api/sensors')
        self.assertEqual(res.status_code, 200, res.get_json())

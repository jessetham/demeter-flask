from tests import utl
from tests.api.base import BaseAPICase

class SensorsAPICase(BaseAPICase):
    def test_create(self):
        utl.add_categories_to_db(self)

        # Test adding a sensor with one missing parameter
        res = self.client.post('/api/sensors', json={'name': 'failure'})
        self.assertEqual(res.status_code, 400, res.get_json())

        # Test adding sensors with the correct parameters
        for sensor in utl.SENSORS:
            res = self.client.post('/api/sensors', json=sensor)
            self.assertEqual(res.status_code, 201, res.get_json())

        # Test adding a sensor that's already been added
        sensor = utl.SENSORS[-1]
        res = self.client.post('/api/sensors', json=sensor)
        self.assertEqual(res.status_code, 400, res.get_json())

        # Test adding a sensor with a category that doesn't exist in db
        # TODO: Add test for issue #4 on GitHub before working on it

    def test_get_single(self):
        utl.add_categories_to_db(self)
        utl.add_sensors_to_db(self)

        # Test getting a sensor that hasn't been created yet
        res = self.client.get('/api/sensors/42')
        self.assertEqual(res.status_code, 404, res.get_json())

        # Test getting a sensor that has been created
        res = self.client.get('/api/sensors/1')
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_get_multiple(self):
        utl.add_categories_to_db(self)
        utl.add_sensors_to_db(self)

        # Get the list of sensor stored in the db
        res = self.client.get('/api/sensors')
        self.assertEqual(res.status_code, 200, res.get_json())

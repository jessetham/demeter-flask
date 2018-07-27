from tests import utl
from tests.api.base import BaseAPICase

class ReadingsAPICase(BaseAPICase):
    def test_create(self):
        utl.add_categories_to_db(self)
        utl.add_sensors_to_db(self)

        # Test adding a reading to a sensor that doesn't exist
        res = self.client.post('api/sensors/42/readings',
            json={'data': 404, 'category': 'temperature'}
        )
        self.assertEqual(res.status_code, 404, res.get_json())

        sensor = utl.SENSORS[-1]
        # Test adding a reading with a category that doesn't exist
        res = self.client.post('api/sensors/{}/readings'.format(sensor['id']),
            json={'data': 400, 'category': 'failure'}
        )
        self.assertEqual(res.status_code, 400, res.get_json())

        # Test adding a reading with no data parameter
        res = self.client.post('api/sensors/{}/readings'.format(sensor['id']),
            json={'category': 'failure'}
        )
        self.assertEqual(res.status_code, 400, res.get_json())

        # Test adding a reading with no category parameter
        res = self.client.post('api/sensors/{}/readings'.format(sensor['id']),
            json={'data': 400}
        )
        self.assertEqual(res.status_code, 400, res.get_json())

        # Add valid readings
        utl.add_readings_to_db(self)

    def test_get_single(self):
        pass

    def test_get_multiple(self):
        pass

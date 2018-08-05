from random import randint
from tests import utl
from tests.api.base import BaseAPICase

class ReadingsAPICase(BaseAPICase):
    def test_create(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()

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
        for category in sensor['categories']:
            reading = {
                'data': randint(utl.READING_LOWER_LIMIT, utl.READING_UPPER_LIMIT),
                'category': category
            }
            res = self.client.post('/api/sensors/{}/readings'.format(sensor['id']),
                json=reading
            )
            self.assertEqual(res.status_code, 201, res.get_json())

    def test_get_single(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        utl.add_readings_to_db()

        # Test getting a reading from a sensor that doesn't exist
        res = self.client.get('api/sensors/42/readings/1')
        self.assertEqual(res.status_code, 404, res.get_json())

        sensor = utl.SENSORS[-1]
        # Test getting a reading that doesn't exist
        res = self.client.get('api/sensors/{}/readings/42'.format(sensor['id']))
        self.assertEqual(res.status_code, 404, res.get_json())

        readings = [reading['id'] for reading in utl.READINGS if reading['sensor'] == sensor['id']]
        # Test getting readings that do exist
        for reading in readings:
            res = self.client.get('api/sensors/{}/readings/{}'.format(sensor['id'], reading))
            self.assertEqual(res.status_code, 200, res.get_json())

    def test_get_multiple(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        utl.add_readings_to_db()

        # Test getting readings from a sensor that doesn't exist
        res = self.client.get('api/sensors/42/readings')
        self.assertEqual(res.status_code, 404, res.get_json())

        sensor = utl.SENSORS[-1]
        # Test getting readings from a valid sensor
        res = self.client.get('api/sensors/{}/readings'.format(sensor['id']))
        self.assertEqual(res.status_code, 200, res.get_json())

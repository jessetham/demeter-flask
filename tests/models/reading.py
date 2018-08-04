from tests import utl
from app.models.reading import Reading
from tests.base import BaseCase

class ReadingModelCase(BaseCase):
    def test_add_category(self):
        utl.add_categories_to_db()
        category = utl.CATEGORIES[-1]
        r = Reading()

        # Test adding a category to a reading
        r.add_category(category['name'])
        self.assertEqual(r.category.name, category['name'])

    def test_add_sensor(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        sensor = utl.SENSORS[-1]
        r = Reading()

        # Test adding a sensor to a reading
        r.add_sensor(sensor['name'])
        self.assertEqual(r.sensor.name, sensor['name'])

    def test_from_and_to_dict(self):
        pass

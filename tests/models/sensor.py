from tests import utl
from app.models.sensor import Sensor
from tests.base import BaseCase


class SensorModelCase(BaseCase):
    def test_are_valid_sensors(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()

        # Test checking an array with valid sensors
        sensors = [sensor["name"] for sensor in utl.SENSORS]
        valid = Sensor.are_valid_sensors(sensors)
        self.assertEqual(valid, True)

        sensors.append("failure")
        # Test checking an array with one invalid sensor
        valid = Sensor.are_valid_sensors(sensors)
        self.assertEqual(valid, False)

        # Test checking an empty list
        valid = Sensor.are_valid_sensors([])
        self.assertEqual(valid, False)

    def test_add_and_remove_categories(self):
        utl.add_categories_to_db()
        sensor = utl.SENSORS[-1]
        s = Sensor()

        # Test adding categories to a sensor
        s.add_categories(sensor["categories"])
        self.assertEqual(
            set([category.name for category in s.categories]), set(sensor["categories"])
        )
        self.assertEqual(len(s.categories), len(sensor["categories"]))

        s.remove_categories(sensor["categories"])
        self.assertEqual(len(s.categories), 0)

    def test_from_and_to_dict(self):
        utl.add_categories_to_db()
        sensor = utl.SENSORS[-1]
        s = Sensor()

        # Test using the from_dict() method
        s.from_dict(sensor)
        self.assertEqual(s.name, sensor["name"])
        self.assertEqual(
            set([category.name for category in s.categories]), set(sensor["categories"])
        )

        # Test using the to_dict() method
        s_dict = s.to_dict()
        self.assertEqual(s_dict["name"], sensor["name"])
        self.assertEqual(
            set([category["name"] for category in s_dict["categories"]]),
            set(sensor["categories"]),
        )

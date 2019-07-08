from tests import utl
from tests.api.base import BaseAPICase


class SensorsAPICase(BaseAPICase):
    def test_create(self):
        utl.add_categories_to_db()

        # Test adding a sensor with one missing parameter
        res = self.client.post("/api/sensors", json={"name": "failure"})
        self.assertEqual(res.status_code, 400, res.get_json())

        sensor = utl.SENSORS[-1]
        # Test adding sensors with the correct parameters
        res = self.client.post("/api/sensors", json=sensor)
        self.assertEqual(res.status_code, 201, res.get_json())

        # Test adding a sensor that's already been added
        res = self.client.post("/api/sensors", json=sensor)
        self.assertEqual(res.status_code, 400, res.get_json())

        # Test adding a sensor with a category that doesn't exist in db
        res = self.client.post(
            "/api/sensors", json={"name": "failure", "categories": ["failure"]}
        )
        self.assertEqual(res.status_code, 400, res.get_json())

    def test_get_single(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()

        # Test getting a sensor that hasn't been created yet
        res = self.client.get("/api/sensors/42")
        self.assertEqual(res.status_code, 404, res.get_json())

        # Test getting a sensor that has been created
        res = self.client.get("/api/sensors/1")
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_get_multiple(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()

        # Get the list of sensor stored in the db
        res = self.client.get("/api/sensors")
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_get_sensor_categories(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()

        # Test getting categories from a sensor that doesn't exist
        res = self.client.get("/api/sensors/42/categories")
        self.assertEqual(res.status_code, 404, res.get_json())

        # Test getting categories from a sensor that does exist
        res = self.client.get("/api/sensors/1/categories")
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_add_sensor_categories(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        valid_categories = [category["name"] for category in utl.CATEGORIES]

        sensor = utl.SENSORS[-1]
        # Test adding missing categories to sensors
        missing_categories = [
            category
            for category in valid_categories
            if category not in sensor["categories"]
        ]
        res = self.client.patch(
            "/api/sensors/{}/categories/add".format(sensor["id"]),
            json={"categories": missing_categories},
        )
        self.assertEqual(res.status_code, 204)

        # Test adding a category that doesn't exist
        res = self.client.patch(
            "/api/sensors/{}/categories/add".format(sensor["id"]),
            json={"categories": ["failure"]},
        )
        self.assertEqual(res.status_code, 400)

    def test_remove_sensor_categories(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()

        sensor = utl.SENSORS[-1]
        # Test removing available categories from sensors
        res = self.client.patch(
            "/api/sensors/{}/categories/remove".format(sensor["id"]),
            json={"categories": sensor["categories"]},
        )
        self.assertEqual(res.status_code, 204)

        # Test removing a category that doesn't exist
        res = self.client.patch(
            "/api/sensors/{}/categories/remove".format(sensor["id"]),
            json={"categores": ["failure"]},
        )
        self.assertEqual(res.status_code, 400)

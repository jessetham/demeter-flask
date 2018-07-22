from tests import utl
from tests.api.base import BaseAPICase

class CategoriesAPICase(BaseAPICase):
    def test_create(self):
        # Test adding a category with one missing parameter
        res = self.client.post('/api/categories', json={'name': 'failure'})
        self.assertEqual(res.status_code, 400, res.get_json())

        # Test adding categories with correct parameters
        for category in utl.CATEGORIES:
            res = self.client.post('/api/categories', json=category)
            self.assertEqual(res.status_code, 201, res.get_json())

        # Test adding a category that's already been added
        category = utl.CATEGORIES.pop()
        res = self.client.post('/api/categories', json=category)
        self.assertEqual(res.status_code, 400, res.get_json())

    def test_get_single(self):
        utl.add_categories_to_db(self)

        # Test getting a category that doesn't exist in the db
        res = self.client.get('/api/categories/42')
        self.assertEqual(res.status_code, 404, res.get_json())

        # Test getting a category that has been created
        res = self.client.get('/api/categories/1')
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_get_multiple(self):
        utl.add_categories_to_db(self)

        # Test getting multiple categories from the db
        res = self.client.get('/api/categories')
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_get_categories_of_sensor(self):
        utl.add_categories_to_db(self)
        utl.add_sensors_to_db(self)

        # Test getting categories from a sensor that doesn't exist
        res = self.client.get('/api/sensors/42/categories')
        self.assertEqual(res.status_code, 404, res.get_json())

        # Test getting categories from a sensor that does exist
        res = self.client.get('/api/sensors/1/categories')
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_add_categories_to_sensor(self):
        # TODO: Write tests before adding issue #4 in GitHub
        pass

    def test_remove_categories_from_sensor(self):
        # TODO: Write tests before adding issue #4 in GitHub
        pass

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
        category = utl.CATEGORIES[-1]
        res = self.client.post('/api/categories', json=category)
        self.assertEqual(res.status_code, 400, res.get_json())

    def test_get_single(self):
        utl.add_categories_to_db()

        # Test getting a category that doesn't exist in the db
        res = self.client.get('/api/categories/42')
        self.assertEqual(res.status_code, 404, res.get_json())

        # Test getting a category that has been created
        res = self.client.get('/api/categories/1')
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_get_multiple(self):
        utl.add_categories_to_db()

        # Test getting multiple categories from the db
        res = self.client.get('/api/categories')
        self.assertEqual(res.status_code, 200, res.get_json())

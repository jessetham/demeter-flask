from tests import utl
from app.models.category import Category
from tests.base import BaseCase

class CategoryModelCase(BaseCase):
    def test_are_valid_categories(self):
        utl.add_categories_to_db()

        # Test checking an array with valid categories
        categories = [category['name'] for category in utl.CATEGORIES]
        valid = Category.are_valid_categories(categories)
        self.assertEqual(valid, True)

        categories.append('failure')
        # Test checking an array with one invalid category
        valid = Category.are_valid_categories(categories)
        self.assertEqual(valid, False)

    def test_from_and_to_dict(self):
        category = utl.CATEGORIES[-1]
        c = Category()

        # Test using the from_dict() method
        c.from_dict(category)
        self.assertEqual(c.name, category['name'])
        self.assertEqual(c.units, category['units'])

        # Test using the to_dict() method
        c_dict = c.to_dict()
        self.assertEqual(c_dict['name'], category['name'])
        self.assertEqual(c_dict['units'], category['units'])

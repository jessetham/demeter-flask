from tests import utl
from app.models.category import Category
from tests.base import BaseCase

class CategoryModelCase(BaseCase):
    def test_are_valid_categories(self):
        utl.add_categories_to_db(self)

        # Test checking an array with valid categories
        categories = [category['name'] for category in utl.CATEGORIES]
        valid = Category.are_valid_categories(categories)
        self.assertEqual(valid, True)

        categories.append('failure')
        # Test checking an array with one invalid category
        valid = Category.are_valid_categories(categories)
        self.assertEqual(valid, False)

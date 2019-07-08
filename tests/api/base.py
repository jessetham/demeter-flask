from tests.base import BaseCase


class BaseAPICase(BaseCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()

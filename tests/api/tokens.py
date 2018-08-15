import base64
from tests import utl
from tests.api.base import BaseAPICase

class TokensAPICase(BaseAPICase):
    def test_get_token(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        utl.add_users_to_db()
        user = utl.USERS[-1]

        # Test that we can login with the correct credentials
        login_info = (user['name'] + ':' + user['password']).encode()
        res = self.client.get('/api/tokens',
            headers={'Authorization': 'Basic ' + base64.b64encode(login_info).decode('utf-8')}
        )
        self.assertEqual(res.status_code, 200, res.get_json())

        # Test that we get an error when accessing the route without auth
        res = self.client.get('/api/tokens')
        self.assertEqual(res.status_code, 401, res.get_json())

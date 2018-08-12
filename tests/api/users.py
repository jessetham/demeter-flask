from tests import utl
from tests.api.base import BaseAPICase

class UsersAPICase(BaseAPICase):
    def test_create(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()

        # Test adding a user with one missing parameter
        res = self.client.post('/api/users', json={'name': 'failure'})
        self.assertEqual(res.status_code, 400, res.get_json())
        res = self.client.post('/api/users', json={'sensors': ['failure']})
        self.assertEqual(res.status_code, 400, res.get_json())

        user = utl.USERS[-1]
        # Test adding a user with the correct parameters
        res = self.client.post('/api/users', json=user)
        self.assertEqual(res.status_code, 201, res.get_json())

        # Test adding a user that's already in the database
        res = self.client.post('/api/users', json=user)
        self.assertEqual(res.status_code, 400, res.get_json())

        # Test adding a user with a sensor that doesn't exist
        res = self.client.post('/api/users', json={'name': 'failure', 'sensors': ['failure']})
        self.assertEqual(res.status_code, 400, res.get_json())

    def test_get_single(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        utl.add_users_to_db()

        # Test getting a user that doesn't exist
        res = self.client.get('/api/users/42')
        self.assertEqual(res.status_code, 404, res.get_json())

        user = utl.USERS[-1]
        # Test getting a user that does exist
        res = self.client.get('/api/users/{}'.format(user['id']))
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_get_multiple(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        utl.add_users_to_db()

        # Test getting multiple users
        res = self.client.get('/api/users')
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_get_user_sensors(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        utl.add_users_to_db()

        # Test getting sensors from a user that doesn't exist
        res = self.client.get('/api/users/42/sensors')
        self.assertEqual(res.status_code, 404, res.get_json())

        user = utl.USERS[-1]
        # Test getting sensors from a user that does exist
        res = self.client.get('/api/users/{}/sensors'.format(user['id']))
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_add_user_sensors(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        utl.add_users_to_db()
        valid_sensors = [sensor['name'] for sensor in utl.SENSORS]

        user = utl.USERS[-1]
        # Test adding sensors to a user
        missing_sensors = [sensor for sensor in valid_sensors if sensor \
            not in user['sensors']]
        res = self.client.patch(
            '/api/users/{}/sensors/add'.format(user['id']),
            json={'sensors': missing_sensors}
        )
        self.assertEqual(res.status_code, 204)

        # Test adding a sensor that doesn't exist
        res = self.client.patch(
            '/api/users/{}/sensors/add'.format(user['id']),
            json={'sensors': ['failure']}
        )
        self.assertEqual(res.status_code, 400)

    def test_remove_user_sensors(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        utl.add_users_to_db()

        user = utl.USERS[-1]
        # Test removing sensors from a user
        res = self.client.patch(
            '/api/users/{}/sensors/remove'.format(user['id']),
            json={'sensors': user['sensors']}
        )
        self.assertEqual(res.status_code, 204)

        # Test removing an invalid sensor
        res = self.client.patch(
            '/api/users/{}/sensors/remove'.format(user['id']),
            json={'sensors': ['failure']}
        )
        self.assertEqual(res.status_code, 400)

    def test_change_user_password(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        utl.add_users_to_db()

        user = utl.USERS[-1]
        # Test changing the password with an invalid old password
        res = self.client.patch(
            '/api/users/{}/password'.format(user['id']),
            json={'old': 'failure', 'new': 'failure'}
        )
        self.assertEqual(res.status_code, 400)

        # Test changing the password with the correct old password
        res = self.client.patch(
            '/api/users/{}/password'.format(user['id']),
            json={'old': user['password'], 'new': 'failure'}
        )
        self.assertEqual(res.status_code, 204)

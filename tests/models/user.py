from werkzeug.security import generate_password_hash, check_password_hash
from tests import utl
from app.models.user import User
from tests.base import BaseCase

class UserModelCase(BaseCase):
    def test_add_and_remove_sensors(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        user = utl.USERS[-1]
        u = User()

        # Test adding sensors to a user
        u.add_sensors(user['sensors'])
        self.assertEqual(
            set([sensor.name for sensor in u.sensors]),
            set(user['sensors']))
        self.assertEqual(len(u.sensors), len(user['sensors']))

        # Test removing sensors from a user
        u.remove_sensors(user['sensors'])
        self.assertEqual(len(u.sensors), 0)

    def test_set_and_check_password(self):
        u = User()
        password = 'supersecurepassword'

        # Check that the password is correctly set and hashed
        u.set_password(password)
        self.assertTrue(check_password_hash(u.password_hash, password))

        # Check that the check_password method returns the expected response
        self.assertTrue(u.check_password(password))

    def test_get_check_and_revoke_token(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        utl.add_users_to_db()
        user = User.get_all()[-1]

        # Check that a token gets registered to the user
        token = user.get_token()
        self.assertEqual(token, user.token)

        # Check that we recieve the same token when requesting within the timeout
        self.assertEqual(token, user.get_token())

        # Test that the check_token method works
        self.assertEqual(User.check_token(token), user)

        # Test that the revoke_token method works
        user.revoke_token()
        self.assertEqual(User.check_token(token), None)
        self.assertNotEqual(user.get_token(), token)

    def test_from_and_to_dict(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        user = utl.USERS[-1]
        u = User()

        # Test converting from dict to object
        u.from_dict(user)
        self.assertEqual(u.name, user['name'])
        self.assertTrue(check_password_hash(u.password_hash, user['password']))
        self.assertEqual(
            set([sensor.name for sensor in u.sensors]),
            set(user['sensors']))

        # Test converting from object to dict
        u_dict = u.to_dict()
        self.assertEqual(u_dict['name'], user['name'])
        self.assertTrue(check_password_hash(u_dict['password_hash'], user['password']))
        self.assertEqual(
            set([sensor['name'] for sensor in u_dict['sensors']]),
            set(user['sensors'])
        )

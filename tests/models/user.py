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

    def test_from_and_to_dict(self):
        utl.add_categories_to_db()
        utl.add_sensors_to_db()
        user = utl.USERS[-1]
        u = User()

        # Test converting from dict to object
        u.from_dict(user)
        self.assertEqual(u.name, user['name'])
        self.assertEqual(
            set([sensor.name for sensor in u.sensors]),
            set(user['sensors']))

        # Test converting from object to dict
        u_dict = u.to_dict()
        self.assertEqual(u_dict['name'], user['name'])
        self.assertEqual(
            set([sensor['name'] for sensor in u_dict['sensors']]),
            set(user['sensors'])
        )

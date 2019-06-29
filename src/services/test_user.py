from unittest import TestCase, main
from unittest.mock import Mock
from . import UserService
import bcrypt

class TestUserServiceFindByEmailAndPassword(TestCase):
    def setUp(self):
        email = 'j.doe@example.com'
        password = 'hashedpass'
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_obj = {'email': email, 'password': hashed_pass}
        mock = Mock()
        mock.find_one.return_value = user_obj
        self.email = email
        self.password = password
        self.user_obj = user_obj
        self.mock = mock
        self.service = UserService(mock)

    def test_returns_obj(self):
        result = self.service.find_by_email_and_password(self.email, self.password)
        self.assertDictEqual(result, self.user_obj)

    def test_find_one_called(self):
        result = self.service.find_by_email_and_password(self.email, self.password)
        self.mock.find_one.assert_called_with({'email': self.email})

class TestUserServiceEnsureAdminUser(TestCase):

    def setUp(self):
        email = 'j.doe@example.com'
        password = 'hashedpass'
        mock = Mock()
        admin = {
            'first_name': 'Admin',
            'last_name': 'Admin',
            'email': email,
            'role': 'admin'
        }
        self.admin = admin
        self.email = email
        self.password = password
        self.mock = mock
        self.service = UserService(mock)

    def test_update_one_called(self):
        result = self.service.ensure_admin_user(self.email, self.password)
        search, update = self.mock.update_one.call_args[0]
        upsert = self.mock.update_one.call_args[1]['upsert']
        self.assertEqual(search['email'], self.email)
        update['$set'].pop('password', None)
        self.assertDictEqual({'$set': self.admin}, update)
        self.assertTrue(upsert)

if __name__ == '__main__':
    main()

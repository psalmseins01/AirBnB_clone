#!/usr/bin/python3

import unittest
from models.base_model import BaseModel
from models.user import User


class TestUser(unittest.TestCase):
    def test_attributes(self):
        user = User()
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(hasattr(user, 'password'))
        self.assertTrue(hasattr(user, 'first_name'))
        self.assertTrue(hasattr(user, 'last_name'))
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")

    def test_instance(self):
        user = User()
        self.assertIsInstance(user, User)
        self.assertIsInstance(user, BaseModel)


if __name__ == '__main__':
    unittest.main()

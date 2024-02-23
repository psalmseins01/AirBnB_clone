#!/usr/bin/python3
"""Defines unittests for models/state.py
Unittest class:
    TestState
"""

import unittest
from models.base_model import BaseModel
from models.state import State


class TestState(unittest.TestCase):
    """Unittest, for the testing of objects and
       attributes of the 'State' class
    """
    def test_attributes(self):
        state = State()
        self.assertTrue(hasattr(state, 'name'))
        self.assertEqual(state.name, "")

    def test_instance(self):
        state = State()
        self.assertIsInstance(state, State)
        self.assertIsInstance(state, BaseModel)


if __name__ == '__main__':
    unittest.main()


#!/usr/bin/python3
"""Defines unittests for models/amenity.py
Unittest class:
    TestAmenity
Unittest methods and attributes:
    test_attributes
    test_instance
"""

import unittest
from models.base_model import BaseModel
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Unittests for testing ojbjects and attributes of the Amenity class."""
    def test_attributes(self):
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, 'name'))
        self.assertEqual(amenity.name, "")

    def test_instance(self):
        amenity = Amenity()
        self.assertIsInstance(amenity, Amenity)
        self.assertIsInstance(amenity, BaseModel)


if __name__ == '__main__':
    unittest.main()

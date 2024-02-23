#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py
"""
#!/usr/bin/python3

import unittest
import os
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()

    def tearDown(self):
        del self.storage

    def test_attributes(self):
        self.assertTrue(hasattr(self.storage, '_FileStorage__file_path'))
        self.assertTrue(hasattr(self.storage, '_FileStorage__objects'))
        self.assertTrue(hasattr(self.storage, 'class_dict'))
        self.assertIsInstance(self.storage.__file_path, str)
        self.assertIsInstance(self.storage.__objects, dict)
        self.assertIsInstance(self.storage.class_dict, dict)

    def test_all(self):
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        obj = BaseModel()
        self.storage.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertIn(key, self.storage.__objects)

    def test_save_reload(self):
        obj = BaseModel()
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.storage.new(obj)
        self.storage.save()
        del self.storage.__objects[key]
        self.storage.reload()
        self.assertIn(key, self.storage.__objects)

    def test_save_file_exists(self):
        self.storage.save()
        self.assertTrue(os.path.exists(self.storage._FileStorage__file_path))

    def test_reload_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.reload()

    def test_reload(self):
        obj = BaseModel()
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        self.assertIn(key, self.storage.__objects)


if __name__ == '__main__':
    unittest.main()

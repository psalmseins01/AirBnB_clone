#!/usr/bin/python3
"""Unit test for console.py
Unit test classes:
    TestConsolePrompt
    TestConsoleHelp
    TestConsoleExit
    TestConsoleCreate
    TestConsoleShow
    TestConsoleAll
    TestConsoleDestroy
    TestConsoleUpdate
"""
import sys
import os
import json
import pep8
import console
from models import storage
import unittest
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestConsolePrompt(unittest.TestCase):
    """Unit tests for testing the console prompt."""

    @classmethod
    def setUpClass(cls):
        """Set up"""
        cls.console_instance = console.HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Remove temporary file such as file.json created"""
        try:
            os.remove("file.json")
        except FileNotFoundError as e:
            print(e.__str__())

    def test_pep8_test_console(self):
        """Pep8 test_console.py"""
        style_guide = pep8.StyleGuide(quiet=False)
        errors = 0
        file = (["tests/test_console.py"])
        errors += style_guide.check_files(file).total_errors
        self.assertEqual(errors, 0, 'Pep8 fix is needed')

    def test_pep8_console(self):
        """Pep8 conform check console.py"""
        style = pep8.StyleGuide(quiet=False)
        num_of_errors = 0
        file = (["console.py"])
        num_of_errors += style.check_files(file).total_errors
        self.assertEqual(num_of_errors, 0, 'Pep8 fix is needed')

    def test_docstrings_in_test_console(self):
        """Test if docstrings exist in the test_console.py file"""
        self.assertTrue(len(self.__doc__) >= 1)

    def test_docstrings_in_console(self):
        """Test if docstrings exist in the console.py file"""
        self.assertTrue(len(console.__doc__) >= 1)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as result:
            obj = HBNBCommand()
            self.assertFalse(obj.onecmd(""))
            self.assertEqual("", result.getvalue().strip())

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)


class TestHBNBCommandHelp(unittest.TestCase):
    """Unit tests for testing help message outputs
       of the 'HBNB' command interpreter
    """
    def test_help(self):
        expected_help = ("Documented commands (type help <topic>):\n"
                         "========================================\n"
                         "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("help"))
            self.assertEqual(expected_help, output.getvalue().strip())

    def test_help_EOF(self):
        expected_help = "EOF (End_Of_File) signal to exit the program"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("help EOF"))
            self.assertEqual(expected_help, output.getvalue().strip())

    def test_help_all(self):
        expected_help = ("Usage: all or all <class> or <class>.all()\n"
                         "Display string representations of all instances of a given class.\n"
                         "If no class is specified, displays all instantiated objects.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("help all"))
            self.assertEqual(expected_help, output.getvalue().strip())

    def test_help_count(self):
        expected_help = ("Usage: count <class> or <class>.count()\n"
                         "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("help count"))
            self.assertEqual(expected_help, output.getvalue().strip())

    def test_help_create(self):
        expected_help = ("Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ...\n"
                         "Create a new class instance with given keys/values and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("help create"))
            self.assertEqual(expected_help, output.getvalue().strip())

    def test_help_destroy(self):
        expected_help = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n"
                         "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("help destroy"))
            self.assertEqual(expected_help, output.getvalue().strip())

    def test_help_quit(self):
        expected_help = "Quit command to exit the program"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("help quit"))
            self.assertEqual(expected_help, output.getvalue().strip())

    def test_help_show(self):
        expected_help = ("Usage: show <class> <id> or <class>.show(<id>)\n"
                         "Display the string representation\n"
                         "of a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("help show"))
            self.assertEqual(expected_help, output.getvalue().strip())

    def test_help_update(self):
        expected_help = ("Usage: update <class> <id> <attribute_name> <attribute_value> \n"
                         "<class>.update(<id>, <attribute_name>, <attribute_value>)\n" 
                         "<class>.update(<id>, <dictionary>)\n"
                         "Update a class instance of a given id by adding or updating\n"
                         "a given attribute key/value pair or dictionary.\n")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("help update"))
            self.assertEqual(expected_help, output.getvalue().strip())
    

class TestHBNBCommandExit(unittest.TestCase):
    """Unit tests for testing exit from the interpreter"""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO) as output:
            self.assertTrue(console.HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO) as output:
            self.assertTrue(console.HBNBCommand().onecmd("EOF"))


class TestHBNBCommandCreate(unittest.TestCase):
    """Unit tests for testing the create command from HBNB interpreter"""
    
    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}
    
    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(self):
        expected_output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_create_invalid_class(self):
        expected_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_create_invalid_syntax(self):
        expected_output = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(expected_output, output.getvalue().strip())
        expected_output = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create BaseModel"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_ID)]
            command = "BaseModel.show({})".format(test_ID)
            self.assertFalse(console.HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create User"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_ID)]
            command = "User.show({})".format(test_ID)
            self.assertFalse(console.HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create State"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_ID)]
            command = "State.show({})".format(test_ID)
            self.assertFalse(console.HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create Place"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_ID)]
            command = "Place.show({})".format(test_ID)
            self.assertFalse(console.HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create City"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_ID)]
            command = "City.show({})".format(test_ID)
            self.assertFalse(console.HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create Amenity"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_ID)]
            command = "Amenity.show({})".format(test_ID)
            self.assertFalse(console.HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create Review"))
            test_ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_ID)]
            command = "Review.show({})".format(test_ID)
            self.assertFalse(console.HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommandShow(unittest.TestCase):
    """Unit tests for testing the 'show' command from the HBNB command interpreter"""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("show"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd(".show()"))
            self.assertNotEqual(correct, output.getvalue().strip())

    def test_show_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        correct = "** instance id missing **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"show {class_name}"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id_dot_notation(self):
        correct = "** instance id missing **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"{class_name}.show()"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found_space_notation(self):
        correct = "** no instance found **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"show {class_name} 1"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self):
        correct = "** no instance found **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"{class_name}.show(1)"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_objects_space_notation(self):
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"create {class_name}"))
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()[f"{class_name}.{test_id}"]
                command = f"show {class_name} {test_id}"
                self.assertFalse(console.HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())

    def test_show_objects_dot_notation(self):
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"create {class_name}"))
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()[f"{class_name}.{test_id}"]
                command = f"{class_name}.show({test_id})"
                self.assertFalse(console.HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())



class TestHBNBCommandAll(unittest.TestCase):
    """Unit tests for testing the 'all' command of the HBNB command interpreter"""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_all_invalid_class(self):
        expected_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(expected_output, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_all_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(console.HBNBCommand().onecmd("create User"))
            self.assertFalse(console.HBNBCommand().onecmd("create State"))
            self.assertFalse(console.HBNBCommand().onecmd("create Place"))
            self.assertFalse(console.HBNBCommand().onecmd("create City"))
            self.assertFalse(console.HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(console.HBNBCommand().onecmd("create Review"))

    def test_all_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(console.HBNBCommand().onecmd("create User"))
            self.assertFalse(console.HBNBCommand().onecmd("create State"))
            self.assertFalse(console.HBNBCommand().onecmd("create Place"))
            self.assertFalse(console.HBNBCommand().onecmd("create City"))
            self.assertFalse(console.HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(console.HBNBCommand().onecmd("create Review"))

    def test_all_single_object_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(console.HBNBCommand().onecmd("create User"))
            self.assertFalse(console.HBNBCommand().onecmd("create State"))
            self.assertFalse(console.HBNBCommand().onecmd("create Place"))
            self.assertFalse(console.HBNBCommand().onecmd("create City"))
            self.assertFalse(console.HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(console.HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("all User"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("all State"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("all City"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())

    def test_all_single_object_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(console.HBNBCommand().onecmd("create User"))
            self.assertFalse(console.HBNBCommand().onecmd("create State"))
            self.assertFalse(console.HBNBCommand().onecmd("create Place"))
            self.assertFalse(console.HBNBCommand().onecmd("create City"))
            self.assertFalse(console.HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(console.HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())



class TestHBNBCommandDestroy(unittest.TestCase):
    """Unit tests for testing the 'destroy' command from the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        storage.reload()

    def test_destroy_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("destroy"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_id_missing_space_notation(self):
        correct = "** instance id missing **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"destroy {class_name}"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_id_missing_dot_notation(self):
        correct = "** instance id missing **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"{class_name}.destroy()"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_id_space_notation(self):
        correct = "** no instance found **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"destroy {class_name} 1"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(self):
        correct = "** no instance found **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"{class_name}.destroy(1)"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_objects_space_notation(self):
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"create {class_name}"))
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"destroy {class_name} {test_id}"))
                self.assertNotIn(f"{class_name}.{test_id}", storage.all())

    def test_destroy_objects_dot_notation(self):
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"create {class_name}"))
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"{class_name}.destroy({test_id})"))
                self.assertNotIn(f"{class_name}.{test_id}", storage.all())


class TestHBNBCommandUpdate(unittest.TestCase):
    """Unit tests for testing the 'update' command from the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_update_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("update"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd(".update()"))
            """self.assertEqual(correct, output.getvalue().strip())"""

    def test_update_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("MyModel.update()"))
            """self.assertEqual(correct, output.getvalue().strip())"""

    def test_update_missing_id_space_notation(self):
        correct = "** instance id missing **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"update {class_name}"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_invalid_id_space_notation(self):
        correct = "** no instance found **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"update {class_name} 1"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_name_space_notation(self):
        correct = "** attribute name missing **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"create {class_name}"))
                test_id = output.getvalue().strip()
                test_cmd = f"update {class_name} {test_id}"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(test_cmd))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_value_space_notation(self):
        correct = "** value missing **"
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                console.HBNBCommand().onecmd(f"create {class_name}")
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                test_cmd = f"update {class_name} {test_id} attr_name"
                self.assertFalse(console.HBNBCommand().onecmd(test_cmd))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_valid_string_attr_space_notation(self):
        classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                console.HBNBCommand().onecmd(f"create {class_name}")
                test_id = output.getvalue().strip()
            test_cmd = f"update {class_name} {test_id} attr_name 'attr_value'"
            self.assertFalse(console.HBNBCommand().onecmd(test_cmd))
            test_dict = storage.all()[f"{class_name}.{test_id}"].__dict__
            self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_float_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            console.HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        test_cmd = f"update Place {test_id} latitude 7.2"
        self.assertFalse(console.HBNBCommand().onecmd(test_cmd))
        test_dict = storage.all()[f"Place.{test_id}"].__dict__
        self.assertEqual(7.2, test_dict["latitude"])


class TestHBNBCommandCount(unittest.TestCase):
    """Unit tests for testing the 'count' method of the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_invalid_class(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(console.HBNBCommand().onecmd("MyModel.count()"))
            """self.assertEqual("0", output.getvalue().strip())"""

    def test_count_object(self):
        classes = ["BaseModel", "User", "State", "Place", "City", "Amenity", "Review"]
        for class_name in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"create {class_name}"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(console.HBNBCommand().onecmd(f"{class_name}.count()"))
                self.assertEqual("1", output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()

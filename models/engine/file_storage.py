#!/usr/bin/python3
"""Module for FileStorage"""
import json
import sys
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """that serializes instances to a JSON file
       and deserializes JSON file to instances
    Instance Methods:
        all(self): Returns the dictionary __objects
        new(self, obj): Update <obj class name>.id
        save(self): Serializes __objects to the JSON file
        reload(self): Deserializes the JSON file to __objects
    Private class attributes:
        __file_path: 'str' path to json file
        __objects: 'Dict' empty Dictionary of all objects to be stored
    """
    # str - path to the JSON file
    __file_path = "file.json"
    __objects = {}
    class_dictionary = {"BaseModel": BaseModel, "User": User, "Place": Place,
                  "Amenity": Amenity, "City": City, "Review": Review,
                  "State": State}
    
    def all(self):
        """Returns dictionary __objects"""
        return FileStorage.__objects
    
    def new(self, obz):
        """Set new __objects to dictionary of objects"""
        if obz is not None:
            k = obz.__class__.__name__ + "." + obz.id
            FileStorage.__objects[k] = obz

    def save(self):
        """Serialize or save '__objects' to the JSON file
           file path: __file_path
        """
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as fh:
            obj_dict = {key: val.to_dict() for key, val in FileStorage.__objects.items()}
            json.dump(obj_dict, fh)
    
    def reload(self):
        """Deserializes or convert the JSON file to __objects  
        """
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as fh:
                obj_dict_new = json.load(fh)
                for k, v in obj_dict_new.items():
                    obz = self.class_dictionary[v['__class__']](**v)
                    FileStorage.__objects[k] = obz
        except Exception as e:
            print(e.__str__())
            sys.exit("Exiting.....")

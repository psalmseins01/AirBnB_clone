#!/usr/bin/python3
"""BaseModel class """

import uuid
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """The BaseModel is the superclass"""

    def __init__(self, *args, **kwargs):
        """Initializing the constructor

        Args:
            *args: arguments in a turple
            **kwargs: keyword arguments
        """
        from models import storage
        """if kwargs:
            for k, v in kwargs.items():
                if "created_at" == k:
                    self.created_at = datetime.strftime(kwargs["created_at"], time)
                elif "updated_at" == k:
                    self.updated_at = datetime.strftime(kwargs["upadated_at"], time)
                else:
                    setattr(self, k, v)"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
            storage.new(self)
            
    def __str__(self) -> str:
        """String representation of the BaseModel class"""
        return ("[{}] ({}) {}".format(__class__.__name__, self.id, self.__dict__))
    
    def save(self):
        """
        Instance method used to:
        - update current datetime
        - invoke save() method
        - save to a serialized file
        """
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values
           of __dict__ of the instance
        """
        """new_dict['created_at'] = new_dict.created_at.isoformat()
        new_dict['updated_at'] = new_dict.updated_at.isoformat()
        new_dict[__class__] = new_dict.self.__class__.__name__"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        return new_dict

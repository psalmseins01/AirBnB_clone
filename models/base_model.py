#!/usr/bin/python3
"""BaseModel class """

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """The BaseModel is the superclass"""

    def __init__(self, *args, **kwargs):
        """Initializing the constructor

        Args:
            *args: arguments in a turple
            **kwargs: keyword arguments
        """
        if kwargs:
            for k, v in kwargs.items():
                if "created_at" == k:
                    self.created_at = datetime.strftime(kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif "updated_at" == k:
                    self.updated_at = datetime.strftime(kwargs["upadated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self) -> str:
        """String representation of the BaseModel class"""
        return "[{}] {()} {}".\
            format(__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        """
        Instance method used to:
        - update current datetime
        - invoke save() method
        - save to a serialized file
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values
           of __dict__ of the instance
        """
        new_dict = self.__dict__.copy()
        new_dict[__class__] = new_dict[self.__class__.__name__]
        new_dict['created_at'] = new_dict['created_at'].isoformat()
        new_dict['updated_at'] = new_dict['updated_at'].isoformat()
        return new_dict

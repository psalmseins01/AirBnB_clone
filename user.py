#!/usr/bin/python3
"""User module, class that inherits from BaseModel"""
from models.base_model import BaseModel


class User(BaseModel):
    """Class used for managing user objects"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

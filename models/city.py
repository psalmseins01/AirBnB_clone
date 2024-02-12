#!/usr/bin/python3
"""City class a subclass of BaseModel"""

from models.base_model import BaseModel


class City(BaseModel):
    """Class for managing city objects"""

    state_id = ""
    name = ""

#!/usr/bin/python3
"""Stae class, modules that inherits from
   BaseModel class
"""
from models.base_model import BaseModel


class State(BaseModel):
    """A subclass of BaseModel class
       Class attribute:
       name: (str)
    """
    name = ""

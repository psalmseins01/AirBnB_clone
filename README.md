# AirBnB Clone - The Console

The console is the initial segment of the AirBnB project at ALXSE, covering fundamental concepts of higher-level programming. The objective of the AirBnB project is to deploy a server that mimics the functionalities of the AirBnB Website (HBnB). A command interpreter is developed in this segment to manage objects for the AirBnB (HBnB) website.

## Functionalities of this Command Interpreter:

- Create a new object (e.g., a new User or a new Place)
- Retrieve an object from a file, a database, etc.
- Perform operations on objects (count, compute stats, etc.)
- Update attributes of an object
- Destroy an object

## Table of Content

- Environment
- Installation
- File Descriptions
- Usage
- Examples of Use
- Bugs
- Authors
- License

## Environment

This project is interpreted and tested on Ubuntu 20.04 LTS using python3 (version 3.8.5).

## Installation

- Clone this repository: `git clone https://github.com/psalmseins01/AirBnB_clone.git`
- Access the AirBnb directory: `cd AirBnB_clone`
- Run hbnb (interactively): `./console` and enter commands
- Run hbnb (non-interactively): `echo "help" | ./console.py`

## File Descriptions

- **console.py**: The console contains the entry point of the command interpreter. List of commands this console currently supports:
    - `EOF`: Exits console
    - `quit`: Exits console
    - `<emptyline>`: Overwrites default empty line method and does nothing
    - `create`: Creates a new instance of `BaseModel`, saves it (to the JSON file), and prints the id
    - `destroy`: Deletes an instance based on the class name and id (saves the change into the JSON file)
    - `show`: Prints the string representation of an instance based on the class name and id
    - `all`: Prints all string representation of all instances based or not on the class name
    - `update`: Updates an instance based on the class name and id by adding or updating attribute (saves the change into the JSON file)

## Models Directory Contains Classes Used for This Project

- **models/base_model.py**: The BaseModel class from which future classes will be derived
    - `def __init__(self, *args, **kwargs)`: Initialization of the base model
    - `def __str__(self)`: String representation of the BaseModel class
    - `def save(self)`: Updates the attribute `updated_at` with the current datetime
    - `def to_dict(self)`: Returns a dictionary containing all keys/values of the instance

Classes inherited from Base Model:

- amenity.py
- city.py
- place.py
- review.py
- state.py
- user.py

## Models Engine Directory Contains File Storage Class

/models/engine directory contains File Storage class that handles JSON serialization and deserialization:

- **file_storage.py**: Serializes instances to a JSON file & deserializes back to instances
    - `def all(self)`: Returns the dictionary __objects
    - `def new(self, obj)`: Sets in __objects the obj with key .id
    - `def save(self)`: Serializes __objects to the JSON file (path: __file_path)
    - `def reload(self)`: Deserializes the JSON file to __objects

## Tests Directory Contains All Unit Test Cases for This Project

/tests directory contains all unit test cases for this project:

- /test_models/test_base_model.py
- /test_models/test_amenity.py
- /test_models/test_city.py
- /test_models/test_file_storage.py
- /test_models/test_place.py
- /test_models/test_review.py
- /test_models/test_state.py
- /test_models/test_user.py

## Examples of Use

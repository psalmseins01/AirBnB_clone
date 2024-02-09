#!/usr/bin/python3
"""Module for the command interpreter 'the console'
   The 'entry point'
"""

import cmd
import re
from models import storage
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State


def parser(self, arg):
    """creates a dictionary from a list of strings"""
    curly_brace = re.search(r"\{(.*?)\}", arg)
    square_brackets = re.search(r"\[(.*?)\]", arg)
    if curly_brace in None:
        if square_brackets is None:
            return [idx.strip(",") for idx in split(arg)]
        else:
            lex = split(arg[:square_brackets.span()[0]])
            ret = [idx.strip(",") for idx in lex]
            ret.append(square_brackets.group())
            return ret
    else:
        lex = split(arg[:square_brackets.span()[0]])
        ret = [idx.strip(",") for idx in lex]
        ret.append(square_brackets.group())
        return ret
    


class HBNBCommand(cmd.Cmd):
    """command interpreter class"""
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self) -> bool:
        """Do nothing if empty line is received"""
        return super().emptyline()
    
    def default(self, line: str) -> None:
        """Default behaviour for the cmd module"""
        dict_args = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        arg_match = re.search(r"\.", line)
        if arg_match:
            line_arg = [line[:arg_match.span()[0]], line[arg_match.span()[1]:]]
            arg_match = re.search(r"\((.*?)\)", line_arg)
            if arg_match is not None:
                command = [line_arg[1][:arg_match.span()[0]], arg_match.group()[1:-1]]
                if command[0] in dict_args.keys():
                    trigger = "{} {}".format(line_arg[0], command[1])
                    return dict_args[command[0]](trigger)
        print("*** Unknown syntax: {}".format(line))
        return super().default(line)

    def do_EOF(self, line):
        """EOF end of file signal"""
        return True
    
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    
    def do_create(self, line):
        """Creates a new instance"""
        try:
            if not line:
                raise SyntaxError()
            obj_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(obj_list)):
                k, v = tuple(obj_list[i].split("="))
                if v[0] == '"':
                    v = v.strip('"').replace("_", " ")
                else:
                    try:
                        v = eval(v)
                    except(SyntaxError, NameError):
                        continue
                kwargs[k] = v
            if kwargs == {}:
                obj = eval(obj_list[0])()
            else:
                obj = eval(obj_list[0])(**kwargs)
                storage.new(obj)
                print(obj.id)
                obj.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation
           of an instance based on the class name and id
        """
        arg_l = parser(arg)
        dict_obj = storage.all()
        if len(arg_l) == 0:
            print("** class name missing **")
        elif arg_l[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_l) == 1:
            print("** instance id missing **")
        elif "{} {}".format(arg_l[0], arg_l[1]) not in dict_obj:
            print("** no instance found **")
        else:
            print(dict_obj["{}.{}".format(arg_l[0], arg_l[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
           Delete a class instance of a given id.
        """
        arg_l = parser(arg)
        dict_obj = storage.all()
        if len(arg_l) == 0:
            print("** class name missing **")
        elif arg_l[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_l) == 1:
            print("** instance id missing **")
        elif "{} {}".format(arg_l[0], arg_l[1]) not in dict_obj.keys():
            print("** no instance found **")
        else:
            del dict_obj["{}.{}".format(arg_l[0], arg_l[1])]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances of 
           a given class
           If no class is specified, display all objects
           Usage: all or all <class> or <class>.all()
        """
        arg_l = parser(arg)
        if len(arg_l) > 0 and arg_l[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obzect = list()
            for obj in storage.all().values():
                if len(arg_l) > 0 and arg_l[0] == obj.__class__.__name__:
                    obzect.append(obj.__str__())
                elif len(arg_l) == 0:
                    obzect.append(obj.__str__())
            print(obzect)
    
    def do_count(self, line):
        """Retrieve the number of instances of a given class
           Usage: count <class> or <class>.count()
        """
        line_arg = parser(line)
        count = 0
        for obj in storage.all().values():
            if line_arg[0] == obj.__class__.__name__:
                count = count + 1
        print(count)

    def do_update(self, line):
        """Updates an instance based on the class name and id 
           by adding or updating attribute (save the change into the JSON file)
           Usage: update <class> <id> <attribute_name> <attribute_value> or
           <class>.update(<id>, <attribute_name>, <attribute_value>) or
           <class>.update(<id>, <dictionary>)
        """
        arg_len = parser(line)
        dict_obj = storage.all()
        if len(arg_len) == 0:
            print("class name missing **")
            return
        if arg_len[0] not in HBNBCommand.__classes:
            print("class doesn't exist")
            return
        if len(arg_len) == 1:
            print("** instance id missing **")
            return
        if "{} {}".format(arg_len[0], arg_len[1]) not in dict_obj.keys():
            print("** no instance found **")
            return
        if len(arg_len) == 2:
            print("** attribute name missing **")
            return
        if len(arg_len) == 3:
            try:
                type(eval(arg_len[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arg_len) == 4:
            obz = dict_obj["{}.{}".format(arg_len[0], arg_len[1])]
            if arg_len[2] in obz.__class__.__dict__.keys():
                vtype = type(obz.__class__.__dict__[arg_len[2]])
                obz.__dict__[arg_len[2]] = vtype(arg_len[3])
            else:
                obz.__dict__[arg_len[2]] = arg_len[3]
        elif type(eval(arg_len[2])) == dict:
            obz = dict_obj["{}.{}".format(arg_len[0], arg_len[1])]
            for key, value in eval(arg_len[2]).items():
                if (key in obz.__class__.__dict__.keys() and
                        type(obz.__class__.__dict__[key]) in {str, int, float}):
                    vtype = type(obz.__class__.__dict__[key])
                    obz.__dict__[key] = vtype(value)
                else:
                    obz.__dict__[key] = value
        storage.save()
        

if __name__ == "__main__":
    HBNBCommand().cmdloop()

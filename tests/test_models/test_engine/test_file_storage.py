#!/usr/bin/python3
""" Module for testing file storage"""
import datetime
import json
import os
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models.city import City


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        self.test_storage = FileStorage()
        self.test_storage._FileStorage__file_path = "test_file.json"
        del_list = []
        for key in self.test_storage._FileStorage__objects:
            del_list.append(key)
        for key in del_list:
            del self.test_storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove test_storage file at end of tests """
        try:
            os.remove('test_file.json')
        except (FileNotFoundError, PermissionError):
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(self.test_storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        new.save()
        for obj in self.test_storage.all().values():
            temp = obj
            self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = self.test_storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.test_storage.reload()
        self.assertFalse(new in self.test_storage._FileStorage__objects)

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        self.test_storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ test_storage file is successfully loaded to __objects """
        # Create new instances for the classes
        amenity = Amenity()
        basemodel = BaseModel()
        city = City()
        place = Place()
        review = Review()
        state = State()
        user = User()
        # Call the new() method on each instance
        self.test_storage.new(amenity)
        self.test_storage.new(basemodel)
        self.test_storage.new(city)
        self.test_storage.new(place)
        self.test_storage.new(review)
        self.test_storage.new(state)
        self.test_storage.new(user)
        # Dump the new instances created to the JSON file
        self.test_storage.save()
        # Load the saved data from the JSON file
        self.test_storage.reload()
        # Retrieve the __object dictionary from FileStorage class
        object_dict = self.test_storage.all()
        # Check if IDs of all instances are present in object_dict
        self.assertIn("Amenity." + amenity.id, object_dict)
        self.assertIn("BaseModel." + basemodel.id, object_dict)
        self.assertIn("City." + city.id, object_dict)
        self.assertIn("Place." + place.id, object_dict)
        self.assertIn("Review." + review.id, object_dict)
        self.assertIn("State." + state.id, object_dict)
        self.assertIn("User." + user.id, object_dict)

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('test_file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            self.test_storage.reload()

    def test_reload_nonexistent_file(self):
        """Test if reload() does nothing if the file does not exist
        """
        # Call save to create the JSON file
        self.test_storage.save()
        try:
            with open(
                    self.test_storage._FileStorage__file_path,
                    "r",
                    encoding="utf-8"
            ) as file:
                file_content = file.read()
        except (FileNotFoundError, PermissionError):
            pass
        self.assertEqual(file_content, "{}")
        # Delete the JSON file
        os.remove("test_file.json")
        with self.assertRaises(FileNotFoundError):
            open(
                self.test_storage._FileStorage__file_path,
                "r",
                encoding="utf-8"
            )
        # Try to load the saved data from the JSON file
        self.test_storage.reload()
        # Check if __objects is empty
        self.assertEqual(self.test_storage.all(), {})

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(self.test_storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls test_storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(self.test_storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(self.test_storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in self.test_storage.all():
            temp = key
            self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object test_storage created """
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(self.test_storage), FileStorage)

    def test_reload_corrupted_file(self):
        """Test if reload() does nothing if the JSON file is has an
        invalid format
        """
        # Open a JSON file
        with open("test_file.json", "w", encoding="utf-8") as file:
            # Create an invalid JSON format in the JSON file
            file.write("Trying to create an invalid JSON file")
        try:
            # Reload the content from the JSON file
            self.test_storage.reload()
        except json.JSONDecodeError:
            pass
        # Check if __objects is still empty
        self.assertEqual(self.test_storage.all(), {})

    def wrong_file_path(self):
        """Test reload with wrong file path
        """
        # create a JSON file with save()
        self.test_storage.save()
        # Modify file path
        self.test_storage._FileStorage__file_path = "new.json"
        # Reload from a different file path
        self.test_storage.reload()
        # Check if __object is still empty
        # since the file path was changed
        self.assertEqual(self.test_storage.all(), {})

    def test_special_characters(self):
        """Test if save() can handle instances with attributes
        containing special characters
        """
        # Create an instance with attributes containing special characters
        timestamp = datetime.datetime.isoformat(datetime.datetime.now())
        user = User(id="Dmi#%*2", created_at=timestamp,
                    updated_at=timestamp, name="John&Doe")
        # Call new() on user
        self.test_storage.new(user)
        # Save user onto the JSON file
        self.test_storage.save()
        # Reload and check if the instance is present
        self.test_storage.reload()
        self.assertIn("User.Dmi#%*2", self.test_storage.all())

    def test_empty_instances(self):
        """Test save() and reload() on empty instances to ensure it
        does not raise any errors
        """
        # Create a User instance
        user = User()
        # Call new() on user
        self.test_storage.new(user)
        # Save user onto the JSON file
        self.test_storage.save()
        # Reload and check if the instance is present
        self.test_storage.reload()
        self.assertIn("User." + user.id, self.test_storage.all())

    def test_new_args(self):
        """Test new() method with more arguments than it takes
        """
        # Raise a TypeError
        with self.assertRaises(TypeError):
            self.test_storage.new(User(), 1)

    def test_reload_args(self):
        """Test new() method with invalid argument type
        """
        # Raise TypeError
        with self.assertRaises(TypeError):
            self.test_storage.reload(None)

    def test_updated_attributes(self):
        """Test save() and reload() method by modifying the attributes
        of instances
        """
        # Create an instance
        timestamp = datetime.datetime.isoformat(datetime.datetime.now())
        user = User(id="1234", created_at=timestamp,
                    updated_at=timestamp, first_name="John")
        # Call new()
        self.test_storage.new(user)
        # Save the user instance
        self.test_storage.save()
        # Update the user attribute
        user.first_name = "James"
        # Save the change
        self.test_storage.save()
        # Load data from JSON file
        self.test_storage.reload()
        # Get the User instance from __objects
        user_obj = self.test_storage.all()["User." + user.id]
        # Check if the updated attribute is reflected
        self.assertEqual(user_obj.first_name, "James")

    def test_deleted_instance(self):
        """Test reload() and save() methods after deleting an instance
        """
        # Create an instance
        time = datetime.datetime.isoformat(datetime.datetime.now())
        place = Place(id="12k34", created_at=time, updated_at=time,
                      first_name="John")
        # Call place()
        self.test_storage.new(place)
        # Save the place instance
        self.test_storage.save()
        # Delete the place instance and save()
        del self.test_storage._FileStorage__objects["Place." + place.id]
        self.test_storage.save()
        # Reload and check if the removed instance is still absent
        self.test_storage.reload()
        self.assertNotIn("Place." + place.id, self.test_storage.all())

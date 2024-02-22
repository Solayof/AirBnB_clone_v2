#!/usr/bin/python3
""" Module for testing db storage"""
import unittest
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.user import User
from models import storage


class test_dbStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = Amenity()
        storage.new(new)
        storage.save()
        self.assertIn(new.to_dict(), storage.all().values())

    def testt_all(self):
        """Test all method of the db storage"""
        self.assertIsInstance(storage.all(), dict)

    def test_save(self):
        """Test save method of the db storage"""
        instance = User()
        instance.save()
        user_id = instance.id
        storage.pen.execute(
            f"SELECT id FROM users WHERE BINARY  LIKE {user_id}")
        self.assertEqual(storage.pen.fetchone(), user_id)

    def test_delete(self):
        """Test delete method of db storage"""
        instance = Place()
        instance.save()
        user_id = instance.id
        instance.delete()
        # commit the delete
        instance.save()
        result = storage.pen.execute(f"SELECT id FROM places")
        ids = [row[0] for row in result]
        self.assertNotIn(user_id, ids)

    def test_classes(self):
        """Test the classes"""
        user = User()
        user.save()
        self.assertIn(user.to_dict(), storage.all(User).values())
        state = State()
        state.save()
        self.assertIn(state.to_dict(), storage.all(State).values())
        place = Place()
        place.save()
        self.assertIn(place.to_dict(), storage.all(Place).values())
        city = City()
        city.save()
        self.assertIn(city.to_dict(), storage.all(City).values())
        amenity = Amenity()
        amenity.save()
        self.assertIn(amenity.to_dict(), storage.all(Amenity).values())
        # test the all method of the db storage with the classes
        all_dict = storage.all().values()
        self.assertIn(amenity.to_dict(), all_dict)
        self.assertIn(user.to_dict(), all_dict)
        self.assertIn(state.to_dict(), all_dict)
        self.assertIn(place.to_dict(), all_dict)
        self.assertIn(city.to_dict(), all_dict)


if __name__ == "__main__":
    unittest.main()

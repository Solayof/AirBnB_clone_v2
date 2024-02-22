#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
import datetime
from models.amenity import Amenity


class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ """
        new = self.value(name="")
        self.assertEqual(type(new.name), str)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = Amenity(**n)
        new.save()
        self.assertFalse(new.created_at == new.updated_at)

    def test_to_method(self) -> None:
        """test to_dict method
        """
        obj_dict = self.value().to_dict()
        self.assertEqual(obj_dict["__class__"], "Amenity")
        self.assertIsInstance(obj_dict["created_at"], str)
        self.assertIsInstance(obj_dict["updated_at"], str)

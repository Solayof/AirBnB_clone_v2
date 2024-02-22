#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import models
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except:
            pass
        
    def test_init(self):
        """Test initialization of a BaseModel instance with no
        arguments passed
        """
        base_model = BaseModel()
        base_model.save()
        # check if id is a str
        self.assertIsInstance(base_model.id, str)
        # check updated_at and created_at are datetime obj
        self.assertIsInstance(base_model.updated_at, datetime.datetime)
        self.assertIsInstance(base_model.created_at, datetime.datetime)
        # check if base_model is an instance of BaseModel
        self.assertIsInstance(base_model, BaseModel)
        # check if base_model is a valid object __class__
        self.assertTrue(hasattr(base_model, "__class__"))
        # check if calling new() was successful
        self.assertIn(base_model, models.storage.all().values())

    def test_default(self):
        """ test default """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ Test kwargs """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ Test kwards with int """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        base_model = BaseModel()
        basemodel_dict = base_model.__dict__.copy()
        print(basemodel_dict)
        basemodel_str =\
            "[BaseModel] ({}) {}".format(base_model.id, basemodel_dict)
        self.assertEqual(str(base_model), basemodel_str)

    def test_todict(self):
        """ """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}
        new_instance = self.value(**n)
        self.assertIn('Name', new_instance.__dict__)
        self.assertIn('test', new_instance.__dict__.values())

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        new.save()
        self.assertFalse(new.created_at == new.updated_at)

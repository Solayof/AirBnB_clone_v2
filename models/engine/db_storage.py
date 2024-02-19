#!/usr/bin/python3
""" This module defines a class to manage file storage for hbnb clone """
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """ This class manages storage of hbnb models using MySQL """
    __engine = None
    __session = None
    all_tables = [User, State, City, Amenity, Place, Review]

    def __init__(self):
        """Initializes a DBStorage instance
        """
        username = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        hostname = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        running_environment = getenv("HBNB_ENV")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                username,
                password,
                hostname,
                database
                ),
            pool_pre_ping=True
        )
        # if program is being run in a testing environment clear all tables
        # so as to not interfere with the tests
        if running_environment == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Returns a dictionary of all objects. If a table is specified,
        It will return all objects of the specified table

        Args:
            cls (Class, optional): The table to query. Defaults to None.

        Returns:
            dict: A dictionary of all the objects
        """
        all_objects = {}
        if cls and cls in self.all_tables:
            objects = self.__session.query(cls).all()
            for obj in objects:
                key = f"{obj.__class__.__name__}.{obj.id}"
                all_objects[key] = obj
        else:
            for table in self.all_tables:
                objects = self.__session.query(table).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    all_objects[key] = obj

        return all_objects

    def new(self, obj):
        """Adds an object to the current database session

        Args:
            obj (instance of a class): An instance of a class
        """
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session

        Args:
            obj (instance, optional): Object to delete. Defaults to None.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and establishes a session from
        the engine
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))

    def close_session(self):
        """Closes the current database session
        """
        self.__session.remove()

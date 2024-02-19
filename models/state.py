#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    # storage_type = getenv("HBNB_TYPE_STORAGE")

    # Relationship for DBStorage
    # if storage_type == "db":
    cities = relationship("City", backref="state",
                          cascade="all, delete, delete-orphan")

    # Getter attribute for FileStorage
    # else:
    @property
    def cities(self):
        """Returns the list of City instances with
        state_id equals to the current State.id.
        It will be the FileStorage relationship
        between State and City

        Returns:
            list: List of all cities belonging to the current State
            instance
        """
        all_cities = []
        city_items = models.storage.all(City).values()
        for city in city_items:
            if self.id == city.states_id:
                all_cities.append(city)
        return all_cities

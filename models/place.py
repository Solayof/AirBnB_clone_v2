#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.review import Review
import models

place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey(
        "places.id"), primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey(
        "amenities.id"), primary_key=True, nullable=False),
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    # cities = relationship("City", back_populates="places")
    # user = relationship("User", back_populates="places")

    storage_type = getenv("HBNB_TYPE_STORAGE")
    # for DBStorage
    # if storage_type == "db":
    reviews = relationship("Review", backref="place",
                           cascade="all, delete, delete-orphan")
    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        viewonly=False,
        backref="places"
    )
    # for FileStorage
    # else:

    @property
    def reviews(self):
        """Returns the list of Review instances where
        place_id equals to the current Place.id.
        It will be the FileStorage relationship
        between Place and Review

        Returns:
            list: List of all reviews belonging to the current Place
            instance
        """
        all_reviews = []
        review_items = models.storage.all(Review).values()
        for review in review_items:
            if self.id == review.place_id:
                all_reviews.append(review)
        return all_reviews

    @property
    def amenities(self):
        """Returns the list of Amenity instances based on
        amenity_ids that contains all Amenity.id linked to Place
        It will be the FileStorage relationship
        between Place and Amenity

        Returns:
            list: List of all amenities belonging to the current Place
            instance
        """
        all_amenities = []
        amenity_items = models.storage.all(Amenity).values()
        for amenity in amenity_items:
            if amenity.id in self.amenity_ids:
                all_amenities.append(amenity)
        return all_amenities

    @amenities.setter
    def amenities(self, amenity_instance):
        """Setter for ammenit_ids list

        Args:
            amenity_instance (obj): An object
        """
        if isinstance(amenity_instance, Amenity):
            self.amenity_ids.append(amenity_instance.id)

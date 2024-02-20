#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.review import Review
import models


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
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []
    # for DBStorage
    reviews = relationship("Review", backref="place",
                           cascade="all, delete, delete-orphan")
    # for FileStorage

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
        review_items = models.storage.all(Review)
        for review in review_items:
            if self.id == review.place_id:
                all_reviews.append(review)
        return all_reviews

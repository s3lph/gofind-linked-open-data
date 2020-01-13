# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from untitled_project.server.models.base_model_ import Model
from untitled_project.server import util


class Place(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, name: str=None, latitude: float=None, longitude: float=None, wikidata_id: str=None):  # noqa: E501
        """Place - a model defined in Swagger

        :param id: The id of this Place.  # noqa: E501
        :type id: int
        :param name: The name of this Place.  # noqa: E501
        :type name: str
        :param latitude: The latitude of this Place.  # noqa: E501
        :type latitude: float
        :param longitude: The longitude of this Place.  # noqa: E501
        :type longitude: float
        :param wikidata_id: The wikidata_id of this Place.  # noqa: E501
        :type wikidata_id: str
        """
        self.swagger_types = {
            'id': int,
            'name': str,
            'latitude': float,
            'longitude': float,
            'wikidata_id': str
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'latitude': 'latitude',
            'longitude': 'longitude',
            'wikidata_id': 'wikidata_id'
        }
        self._id = id
        self._name = name
        self._latitude = latitude
        self._longitude = longitude
        self._wikidata_id = wikidata_id

    @classmethod
    def from_dict(cls, dikt) -> 'Place':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Place of this Place.  # noqa: E501
        :rtype: Place
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Place.


        :return: The id of this Place.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Place.


        :param id: The id of this Place.
        :type id: int
        """

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this Place.


        :return: The name of this Place.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Place.


        :param name: The name of this Place.
        :type name: str
        """

        self._name = name

    @property
    def latitude(self) -> float:
        """Gets the latitude of this Place.


        :return: The latitude of this Place.
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: float):
        """Sets the latitude of this Place.


        :param latitude: The latitude of this Place.
        :type latitude: float
        """

        self._latitude = latitude

    @property
    def longitude(self) -> float:
        """Gets the longitude of this Place.


        :return: The longitude of this Place.
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude: float):
        """Sets the longitude of this Place.


        :param longitude: The longitude of this Place.
        :type longitude: float
        """

        self._longitude = longitude

    @property
    def wikidata_id(self) -> str:
        """Gets the wikidata_id of this Place.


        :return: The wikidata_id of this Place.
        :rtype: str
        """
        return self._wikidata_id

    @wikidata_id.setter
    def wikidata_id(self, wikidata_id: str):
        """Sets the wikidata_id of this Place.


        :param wikidata_id: The wikidata_id of this Place.
        :type wikidata_id: str
        """

        self._wikidata_id = wikidata_id

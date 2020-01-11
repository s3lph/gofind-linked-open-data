# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from untitled_project.server.models.base_model_ import Model
from untitled_project.server.models.place import Place  # noqa: F401,E501
from untitled_project.server import util


class ArrayOfPlaces(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self):  # noqa: E501
        """ArrayOfPlaces - a model defined in Swagger

        """
        self.swagger_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'ArrayOfPlaces':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ArrayOfPlaces of this ArrayOfPlaces.  # noqa: E501
        :rtype: ArrayOfPlaces
        """
        return util.deserialize_model(dikt, cls)
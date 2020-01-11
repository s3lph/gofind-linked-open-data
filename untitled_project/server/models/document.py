# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from untitled_project.server.models.base_model_ import Model
from untitled_project.server import util


class Document(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, text: str=None, title: str=None, year: int=None, author: str=None):  # noqa: E501
        """Document - a model defined in Swagger

        :param id: The id of this Document.  # noqa: E501
        :type id: int
        :param text: The text of this Document.  # noqa: E501
        :type text: str
        :param title: The title of this Document.  # noqa: E501
        :type title: str
        :param year: The year of this Document.  # noqa: E501
        :type year: int
        :param author: The author of this Document.  # noqa: E501
        :type author: str
        """
        self.swagger_types = {
            'id': int,
            'text': str,
            'title': str,
            'year': int,
            'author': str
        }

        self.attribute_map = {
            'id': 'id',
            'text': 'text',
            'title': 'title',
            'year': 'year',
            'author': 'author'
        }
        self._id = id
        self._text = text
        self._title = title
        self._year = year
        self._author = author

    @classmethod
    def from_dict(cls, dikt) -> 'Document':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Document of this Document.  # noqa: E501
        :rtype: Document
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Document.


        :return: The id of this Document.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Document.


        :param id: The id of this Document.
        :type id: int
        """

        self._id = id

    @property
    def text(self) -> str:
        """Gets the text of this Document.


        :return: The text of this Document.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text: str):
        """Sets the text of this Document.


        :param text: The text of this Document.
        :type text: str
        """

        self._text = text

    @property
    def title(self) -> str:
        """Gets the title of this Document.


        :return: The title of this Document.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the title of this Document.


        :param title: The title of this Document.
        :type title: str
        """

        self._title = title

    @property
    def year(self) -> int:
        """Gets the year of this Document.


        :return: The year of this Document.
        :rtype: int
        """
        return self._year

    @year.setter
    def year(self, year: int):
        """Sets the year of this Document.


        :param year: The year of this Document.
        :type year: int
        """

        self._year = year

    @property
    def author(self) -> str:
        """Gets the author of this Document.


        :return: The author of this Document.
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author: str):
        """Sets the author of this Document.


        :param author: The author of this Document.
        :type author: str
        """

        self._author = author

# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from untitled_project.server.models.base_model_ import Model
from untitled_project.server import util


class Error(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, code: str=None, message: str=None, debug: str=None):  # noqa: E501
        """Error - a model defined in Swagger

        :param code: The code of this Error.  # noqa: E501
        :type code: str
        :param message: The message of this Error.  # noqa: E501
        :type message: str
        :param debug: The debug of this Error.  # noqa: E501
        :type debug: str
        """
        self.swagger_types = {
            'code': str,
            'message': str,
            'debug': str
        }

        self.attribute_map = {
            'code': 'code',
            'message': 'message',
            'debug': 'debug'
        }
        self._code = code
        self._message = message
        self._debug = debug

    @classmethod
    def from_dict(cls, dikt) -> 'Error':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Error of this Error.  # noqa: E501
        :rtype: Error
        """
        return util.deserialize_model(dikt, cls)

    @property
    def code(self) -> str:
        """Gets the code of this Error.


        :return: The code of this Error.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code: str):
        """Sets the code of this Error.


        :param code: The code of this Error.
        :type code: str
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501

        self._code = code

    @property
    def message(self) -> str:
        """Gets the message of this Error.


        :return: The message of this Error.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this Error.


        :param message: The message of this Error.
        :type message: str
        """

        self._message = message

    @property
    def debug(self) -> str:
        """Gets the debug of this Error.


        :return: The debug of this Error.
        :rtype: str
        """
        return self._debug

    @debug.setter
    def debug(self, debug: str):
        """Sets the debug of this Error.


        :param debug: The debug of this Error.
        :type debug: str
        """

        self._debug = debug
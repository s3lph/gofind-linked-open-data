# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from untitled_project.server.models.array_of_places import ArrayOfPlaces  # noqa: E501
from untitled_project.server.test import BaseTestCase


class TestSearchController(BaseTestCase):
    """SearchController integration test stubs"""

    def test_places_search_location_get(self):
        """Test case for places_search_location_get

        
        """
        query_string = [('latitude', 1.2),
                        ('longitude', 1.2),
                        ('radius', 0),
                        ('limit', 1)]
        response = self.client.open(
            '/places/search/location',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_places_search_name_get(self):
        """Test case for places_search_name_get

        
        """
        query_string = [('name', 'name_example')]
        response = self.client.open(
            '/places/search/name',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

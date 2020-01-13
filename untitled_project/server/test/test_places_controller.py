# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from untitled_project.server.models.error import Error  # noqa: E501
from untitled_project.server.models.place import Place  # noqa: E501
from untitled_project.server.test import BaseTestCase


class TestPlacesController(BaseTestCase):
    """PlacesController integration test stubs"""

    def test_place_id_delete(self):
        """Test case for place_id_delete

        Delete the place identified by the ID in the path.
        """
        response = self.client.open(
            '/place/{id}'.format(id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_id_get(self):
        """Test case for place_id_get

        Fetch the place identified by the ID in the path.
        """
        response = self.client.open(
            '/place/{id}'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_id_patch(self):
        """Test case for place_id_patch

        Update the place identified by the ID in the path.
        """
        body = Place()
        response = self.client.open(
            '/place/{id}'.format(id=56),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_put(self):
        """Test case for place_put

        Add a new place
        """
        body = Place()
        response = self.client.open(
            '/place',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

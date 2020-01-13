# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from untitled_project.server.models.error import Error  # noqa: E501
from untitled_project.server.models.image import Image  # noqa: E501
from untitled_project.server.test import BaseTestCase


class TestImagesController(BaseTestCase):
    """ImagesController integration test stubs"""

    def test_image_id_delete(self):
        """Test case for image_id_delete

        Delete the image identified by the ID in the path.
        """
        response = self.client.open(
            '/image/{id}'.format(id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_image_id_get(self):
        """Test case for image_id_get

        Fetch the image identified by the ID in the path.
        """
        response = self.client.open(
            '/image/{id}'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_image_id_image_get(self):
        """Test case for image_id_image_get

        Fetch the image file belonging to the image object identified by the ID in the path.
        """
        response = self.client.open(
            '/image/{id}/image'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_image_id_patch(self):
        """Test case for image_id_patch

        Update the image identified by the ID in the path.
        """
        body = Image()
        response = self.client.open(
            '/image/{id}'.format(id=56),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_image_put(self):
        """Test case for image_put

        Add a new image
        """
        body = Image()
        response = self.client.open(
            '/image',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

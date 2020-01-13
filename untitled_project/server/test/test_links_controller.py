# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from untitled_project.server.models.array_of_documents import ArrayOfDocuments  # noqa: E501
from untitled_project.server.models.array_of_images import ArrayOfImages  # noqa: E501
from untitled_project.server.models.array_of_integers import ArrayOfIntegers  # noqa: E501
from untitled_project.server.models.error import Error  # noqa: E501
from untitled_project.server.test import BaseTestCase


class TestLinksController(BaseTestCase):
    """LinksController integration test stubs"""

    def test_place_id_documents_get(self):
        """Test case for place_id_documents_get

        Find documents related to the place indicated by the ID in the path.
        """
        response = self.client.open(
            '/place/{id}/documents'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_id_images_get(self):
        """Test case for place_id_images_get

        Find images related to the place indicated by the ID in the path.
        """
        response = self.client.open(
            '/place/{id}/images'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_pid_document_did_delete(self):
        """Test case for place_pid_document_did_delete

        Delete a link between a place identified by pid and a document indicated by did.
        """
        query_string = [('position_in_text', 56)]
        response = self.client.open(
            '/place/{pid}/document/{did}'.format(pid=56, did=56),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_pid_document_did_get(self):
        """Test case for place_pid_document_did_get

        Get the links between a place identified by pid and a document indicated by did.
        """
        response = self.client.open(
            '/place/{pid}/document/{did}'.format(pid=56, did=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_pid_document_did_put(self):
        """Test case for place_pid_document_did_put

        Add a link between a place identified by pid and a document indicated by did.
        """
        query_string = [('position_in_text', 56)]
        response = self.client.open(
            '/place/{pid}/document/{did}'.format(pid=56, did=56),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_pid_image_iid_delete(self):
        """Test case for place_pid_image_iid_delete

        Delete a link between a place identified by pid and an image indicated by iid.
        """
        response = self.client.open(
            '/place/{pid}/image/{iid}'.format(pid=56, iid=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_pid_image_iid_get(self):
        """Test case for place_pid_image_iid_get

        Get the link between a place identified by pid and an image indicated by iid.
        """
        response = self.client.open(
            '/place/{pid}/image/{iid}'.format(pid=56, iid=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_pid_image_iid_put(self):
        """Test case for place_pid_image_iid_put

        Add a link between a place identified by pid and an image indicated by iid.
        """
        response = self.client.open(
            '/place/{pid}/image/{iid}'.format(pid=56, iid=56),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

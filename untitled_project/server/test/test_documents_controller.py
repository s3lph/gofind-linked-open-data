# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from untitled_project.server.models.document import Document  # noqa: E501
from untitled_project.server.models.error import Error  # noqa: E501
from untitled_project.server.test import BaseTestCase


class TestDocumentsController(BaseTestCase):
    """DocumentsController integration test stubs"""

    def test_document_id_delete(self):
        """Test case for document_id_delete

        Delete the document identified by the ID in the path.
        """
        response = self.client.open(
            '/document/{id}'.format(id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_document_id_get(self):
        """Test case for document_id_get

        Fetch the document identified by the ID in the path.
        """
        response = self.client.open(
            '/document/{id}'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_document_id_patch(self):
        """Test case for document_id_patch

        Update the document identified by the ID in the path.
        """
        body = Document()
        response = self.client.open(
            '/document/{id}'.format(id=56),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_document_put(self):
        """Test case for document_put

        Add a new document
        """
        body = Document()
        response = self.client.open(
            '/document',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

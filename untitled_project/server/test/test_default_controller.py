# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from untitled_project.server.models.array_of_documents import ArrayOfDocuments  # noqa: E501
from untitled_project.server.models.array_of_images import ArrayOfImages  # noqa: E501
from untitled_project.server.models.array_of_integers import ArrayOfIntegers  # noqa: E501
from untitled_project.server.models.array_of_places import ArrayOfPlaces  # noqa: E501
from untitled_project.server.models.document import Document  # noqa: E501
from untitled_project.server.models.error import Error  # noqa: E501
from untitled_project.server.models.image import Image  # noqa: E501
from untitled_project.server.models.place import Place  # noqa: E501
from untitled_project.server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

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

    def test_ping_get(self):
        """Test case for ping_get

        
        """
        response = self.client.open(
            '/ping',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_id_delete(self):
        """Test case for place_id_delete

        Delete the place identified by the ID in the path.
        """
        response = self.client.open(
            '/place/{id}'.format(id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_place_id_documents_get(self):
        """Test case for place_id_documents_get

        Find documents related to the place indicated by the ID in the path.
        """
        response = self.client.open(
            '/place/{id}/documents'.format(id=56),
            method='GET')
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

    def test_place_id_images_get(self):
        """Test case for place_id_images_get

        Find images related to the place indicated by the ID in the path.
        """
        response = self.client.open(
            '/place/{id}/images'.format(id=56),
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

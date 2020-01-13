# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from untitled_project.server.test import BaseTestCase


class TestServerController(BaseTestCase):
    """ServerController integration test stubs"""

    def test_ping_get(self):
        """Test case for ping_get

        
        """
        response = self.client.open(
            '/ping',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

import unittest
import json

import server

class TestExperimentSetup(unittest.TestCase):
    def test_post(self):
        server.app.testing = True
        client = server.app.test_client()

        data = dict(levels=3, branches=2)
        response = client.post(
            '/configure',
            data=json.dumps(data)
        )

        # TODO: make sure correct response
        assert data == json.loads(response.get_data())
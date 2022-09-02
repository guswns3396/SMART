import unittest
import json

import server

class TestConfigure(unittest.TestCase):
    def test_post(self):
        server.app.testing = True
        client = server.app.test_client()

        data = {
            0: {
                'scn1': '0-txt1',
                'numbranch': 2
            },
            1: {
                'scn1': '1-txt1',
                'scn2': '1-txt2',
                'numbranch': 0
            }
        }
        response = client.post(
            '/configure',
            data=json.dumps(data)
        )

        # TODO: make sure correct response
        pass
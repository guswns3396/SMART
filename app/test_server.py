import unittest
import json

import server


class TestConfigure(unittest.TestCase):
    def test_createStudy(self):
        server.app.testing = True
        client = server.app.test_client()

        data = {
            'lvls': [
                [
                    '0-txt0'
                ],
                [
                    '1-txt0',
                    '1-txt1',
                ],
                [
                    '2-txt0',
                    '2-txt1',
                ]
            ],
            'p': 2 / 3
        }
        response = client.post(
            '/configure',
            data=json.dumps(data)
        )

        # study created
        self.assertTrue(json.loads(response.get_data()) in server.STUDIES)

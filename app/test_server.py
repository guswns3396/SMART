import unittest
import json

import server


class TestConfigure(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        data = {
            0: {
                'scenarios': ['0-scn1'],
                'questions': [
                    {
                        '0-q1': {
                            '0-a1': -1,
                            '0-a2': 1
                        }
                    },
                    {
                        '0-q2': {
                            '0-a1': -1,
                            '0-a2': 1
                        }
                    }
                ]
            },
            1: {
                'scenarios': ['1-scn1', '1-scn2'],
                'questions': [
                    {
                        '1-q1': {
                            '1-a1': -1,
                            '1-a2': 1
                        }
                    },
                    {
                        '1-q2': {
                            '1-a1': -1,
                            '1-a2': 1
                        }
                    }
                ]
            },
            2: {
                'scenarios': ['2-scn1', '2-scn2'],
                'questions': [
                    {
                        '2-q1': {
                            '2-a1': -1,
                            '2-a2': 1
                        }
                    },
                    {
                        '2-q2': {
                            '2-a1': -1,
                            '2-a2': 1
                        }
                    }
                ]
            },
            'p': 2 / 3
        }
        self.response = self.client.post(
            '/configure',
            data=json.dumps(data)
        )

    def test_createStudy(self):
        # study created
        response = self.response
        data = response.data.decode(response.charset)
        print(data)

    def test_invalidParameters(self):
        pass

    def test_redirectToShowStudyId(self):
        response = self.client.get('/study_id')
        print(response.data.decode(response.charset))

class TestJoin(unittest.TestCase):

    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()


    def test_invalidID(self):
        response = self.client.get('/join/test')
        print(response.data.decode(response.charset))

    def test_validID(self):
        data = {
            0: {
                'scenarios': ['0-scn1'],
                'questions': [
                    {
                        '0-q1': {
                            '0-a1': -1,
                            '0-a2': 1
                        }
                    },
                    {
                        '0-q2': {
                            '0-a1': -1,
                            '0-a2': 1
                        }
                    }
                ]
            },
            1: {
                'scenarios': ['1-scn1', '1-scn2'],
                'questions': [
                    {
                        '1-q1': {
                            '1-a1': -1,
                            '1-a2': 1
                        }
                    },
                    {
                        '1-q2': {
                            '1-a1': -1,
                            '1-a2': 1
                        }
                    }
                ]
            },
            2: {
                'scenarios': ['2-scn1', '2-scn2'],
                'questions': [
                    {
                        '2-q1': {
                            '2-a1': -1,
                            '2-a2': 1
                        }
                    },
                    {
                        '2-q2': {
                            '2-a1': -1,
                            '2-a2': 1
                        }
                    }
                ]
            },
            'p': 2 / 3
        }
        self.client.post('/configure', data=json.dumps(data))
        response = self.client.get('/study_id')
        data = response.data.decode(response.charset)
        study_id = data[10:]
        print(study_id)
        response = self.client.get('/join/'+study_id)
        print(response.data.decode(response.charset))

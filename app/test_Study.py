import unittest
import json

import Study

class TestStudy(unittest.TestCase):
    def test_instantiation(self):
        parameters = {
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
        parameters = json.loads(json.dumps(parameters))
        study = Study.Study(parameters)
        self.assertTrue(isinstance(study, Study.Study))
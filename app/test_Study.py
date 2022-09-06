import unittest
import json

import Study


class TestStudy(unittest.TestCase):
    def test_instantiation(self):
        parameters = {
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
        parameters = json.loads(json.dumps(parameters))
        study = Study.Study(parameters)
        self.assertTrue(isinstance(study, Study.Study))

    def test_tree(self):
        parameters = {
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

        parameters = json.loads(json.dumps(parameters))
        study = Study.Study(parameters)
        study.root.print()
        # TODO: actually assert

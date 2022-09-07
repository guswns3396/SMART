import unittest
import json

import Study


class TestStudy(unittest.TestCase):

    def setUp(self) -> None:
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
        self.parameters = json.loads(json.dumps(parameters))

    def test_instantiation(self):
        study = Study.Study(self.parameters)
        self.assertTrue(isinstance(study, Study.Study))

    def test_tree(self):
        study = Study.Study(self.parameters)
        study.root.print()
        # TODO: actually assert

    def test_initialCount(self):
        study = Study.Study(self.parameters)
        self.assertEqual(0, study.get_node([1, 1]).count)

    def test_count(self):
        study = Study.Study(self.parameters)
        # TODO: add to count

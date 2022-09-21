import unittest
import json

import Study


class TestStudy(unittest.TestCase):

    def setUp(self) -> None:
        parameters = {
            'scenarios': [
                ['0-snc1'],
                ['1-scn1', '1-scn2'],
                ['2-scn1', '2-scn2'],
                ['3-scn1', '3-scn2']
            ],
            'questions': [
                ['1-q1', '1-q2'],
                ['2-q1', '2-q2'],
                ['3-q1', '3-q2']
            ],
            'answers': [
                {'1-a1': 1, '1-a2': 2},
                {'2-a1': 1, '2-a2': 2},
                {'3-a1': 1, '3-a2': 2}
            ],
            'primary_question': {
                'question': 'primary question',
                'answers': {
                    'a1': 1,
                    'a2': 2,
                    'a3': 3,
                    'a4': 4,
                    'a5': 5,
                    'a6': 6,
                    'a7': 7
                }
            },
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

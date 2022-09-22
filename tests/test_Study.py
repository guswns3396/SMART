import unittest

from flaskr.Study import Study

from werkzeug.datastructures import ImmutableMultiDict


class TestStudy(unittest.TestCase):

    def setUp(self) -> None:
        parameters = ImmutableMultiDict([
            ('num_lvls', 2),
            ('prim_q', 'primary question'),
            ('p', 0.7),
            ('scn-a', '1-scn-a'),
            ('scn-b', '1-scn-b'),
            ('scn-a', '2-scn-a'),
            ('scn-b', '2-scn-b')
        ])
        self.parameters = parameters

    def test_instantiation(self):
        study = Study.Study(self.parameters)
        self.assertTrue(isinstance(study, Study.Study))

    def test_invalidParams(self):
        parameters = ImmutableMultiDict([
            ('num_lvls', 2),
            ('prim_q', 'primary question'),
            ('p', 0.7),
            ('scn-a', '1-scn-a'),
            ('scn-b', '1-scn-b')
        ])
        try:
            study = Study.Study(parameters)
        except ValueError as e:
            e2 = ValueError('number of scenarios does not match number of levels:')
            self.assertTrue(type(e) is type(e2) and e.args == e2.args)

    def test_tree(self):
        pass

    def test_initialCount(self):
        study = Study.Study(self.parameters)
        pass

    def test_count(self):
        study = Study.Study(self.parameters)
        # TODO: add to count
